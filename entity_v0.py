"""
Entity v0 Orchestrator
=======================

Main entry point. Runs ONE aggregation cycle:

1. Verify Immutable Core hash (halt if tampered)
2. Pull threats from external intelligence sources
3. Pull threats from social signal channels
4. Dedup against memory
5. Voice-transform each new threat
6. Severity-gate posting (CRITICAL/HIGH to X+TG+feed, MEDIUM to TG+feed, LOW to feed)
7. Post to channels
8. Update feed.json
9. Archive in posted_db
10. Audit log all decisions
11. Heartbeat

Run via the cycle scheduler defined in the operator runbook.

Modes:
  ENTITY_MODE=production  - real posting
  ENTITY_MODE=shadow      - log only, dry_run on all posts
  ENTITY_MODE=dev         - verbose logging, no posting
"""

import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from defense.core_hash_verifier import halt_if_mismatch
from defense.kill_switch import is_triggered as killswitch_triggered, get_state as killswitch_state
from defense.spending_guard import get_summary as spending_summary
from defense.rate_limiter import get_summary as rate_summary
from defense.circuit_breaker import get_status as cb_status

from cognition.memory import (
    get_seen_registry, get_posted_archive, threat_hash
)
from cognition.voice import transform

from perception.intel_aggregator import aggregate as intel_aggregate
from perception.social_intel import scan as social_scan

from action.x_poster import post as post_x
from action.telegram_poster import post as post_telegram
from action.feed_writer import append as feed_append

from continuity.health_monitor import heartbeat
from governance.audit_log import log_event


# ============================================================
# Logging setup
# ============================================================

def setup_logging():
    """Configure logging for the cycle."""
    log_level = logging.INFO
    if os.getenv("ENTITY_MODE") == "dev":
        log_level = logging.DEBUG

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    console.setLevel(log_level)

    # File handler
    file = logging.FileHandler(config.PATHS["entity_log"])
    file.setFormatter(formatter)
    file.setLevel(log_level)

    root = logging.getLogger()
    root.setLevel(log_level)
    root.handlers.clear()
    root.addHandler(console)
    root.addHandler(file)

logger = logging.getLogger("entity")

def _x_posts_last_hour() -> int:
    """Count successful X posts in the trailing 60 minutes (hourly rate spread)."""
    try:
        from db.connection import cursor
        with cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM posted
                WHERE channel = 'x' AND success = true
                  AND posted_at > NOW() - INTERVAL '60 minutes'
            """)
            return cur.fetchone()[0]
    except Exception as e:
        logger.error(f"_x_posts_last_hour failed: {e}")
        return 0




# ============================================================
# Cycle
# ============================================================

def run_cycle():
    """Execute one aggregator cycle."""
    cycle_start = time.time()
    cycle_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    mode = os.getenv("ENTITY_MODE", "shadow").lower()
    dry_run = mode in ("shadow", "dev")

    logger.info(f"=== CYCLE START {cycle_id} (mode={mode}, dry_run={dry_run}) ===")
    log_event("cycle_start", cycle_id=cycle_id, mode=mode)

    # ----------------------------------------------------------
    # 1. SAFETY: verify Immutable Core hash
    # ----------------------------------------------------------
    halt_if_mismatch()
    if config.is_enabled("core_hash_verify"):
        logger.info("[1/9] Core hash verified (TCB integrity OK)")
    else:
        logger.warning("[1/9] Core hash verify DISABLED")

    # ----------------------------------------------------------
    # 1b. SAFETY: check Guardian Safe kill-switch
    # ----------------------------------------------------------
    if killswitch_triggered():
        state = killswitch_state()
        logger.critical(
            "KILL-SWITCH ACTIVE: Guardian Safe triggered halt. "
            "State: %s. Entity will not act this cycle. "
            "Manual reset required before resumption.",
            state,
        )
        log_event("killswitch_halt", **state)
        return  # exit cycle immediately, no perception/cognition/action
    logger.info("[1b/9] Kill-switch OK")

    # ----------------------------------------------------------
    # 2. ENV CHECK
    # ----------------------------------------------------------
    env = config.env_check()
    log_event("env_check", **env)
    missing = [k for k, v in env.items() if not v]
    if missing and mode == "production":
        logger.warning(f"Missing env vars in production mode: {missing}")

    # ----------------------------------------------------------
    # 3. PERCEPTION: pull threats
    # ----------------------------------------------------------
    threats: list[dict] = []

    if config.is_enabled("intel_aggregator"):
        logger.info("[2/9] Intel aggregation...")
        try:
            intel_threats = intel_aggregate()
            threats.extend(intel_threats)
            log_event("intel_collected", count=len(intel_threats))
        except Exception as e:
            logger.error(f"Intel aggregator failed: {e}")
            log_event("intel_error", error=str(e))

    if config.is_enabled("social_intel"):
        logger.info("[3/9] Social intel scan...")
        try:
            social_threats = social_scan()
            threats.extend(social_threats)
            log_event("social_collected", count=len(social_threats))
        except Exception as e:
            logger.error(f"Social intel failed: {e}")
            log_event("social_error", error=str(e))

    logger.info(f"[4/9] Total threats collected: {len(threats)}")

    # ----------------------------------------------------------
    # 4. DEDUP
    # ----------------------------------------------------------
    seen = get_seen_registry()
    seen.prune()  # Remove stale entries

    new_threats = [t for t in threats if not seen.has_seen(t)]
    logger.info(f"[5/9] After dedup: {len(new_threats)} new threats")
    log_event("dedup_complete", total=len(threats), new=len(new_threats))

    # Cap per cycle
    if len(new_threats) > config.MAX_THREATS_PER_CYCLE:
        logger.warning(f"Capping to {config.MAX_THREATS_PER_CYCLE} threats this cycle")
        # Sort by tier (1=most reliable) then process
        new_threats.sort(key=lambda t: t.get("source_tier", 3))
        new_threats = new_threats[:config.MAX_THREATS_PER_CYCLE]

    # ----------------------------------------------------------
    # 5. VOICE TRANSFORM + POSTING
    # ----------------------------------------------------------
    posted_archive = get_posted_archive()
    posted_count = 0
    skipped_count = 0
    error_count = 0

    for idx, threat in enumerate(new_threats, 1):
        threat_id = threat_hash(threat)
        # Assign Entity ID BEFORE transform so X/TG/feed posts all carry the same code.
        try:
            from action.feed_writer import _get_or_create_entity_id
            threat["entity_id"] = _get_or_create_entity_id(threat_id) or threat.get("entity_id")
        except Exception as _e:
            logger.warning(f"entity_id pre-assign failed: {_e}")
        logger.info(f"[6/9] [{idx}/{len(new_threats)}] Processing {threat_id} [{threat.get('entity_id','?')}]: {threat.get('title', '')[:70]}")

        # Mark seen (even if we skip)
        seen.mark_seen(threat)

        try:
            transformed = transform(threat)
        except Exception as e:
            logger.error(f"Transform failed for {threat_id}: {e}")
            log_event("transform_error", threat_id=threat_id, error=str(e))
            error_count += 1
            continue

        if transformed.get("skip"):
            skipped_count += 1
            log_event(
                "threat_skipped",
                threat_id=threat_id,
                reason=transformed.get("skip_reason"),
                source=threat.get("source_name"),
            )
            logger.info(f"  -> Skipped: {transformed.get('skip_reason')}")
            continue

        severity = transformed.get("severity", "MEDIUM")
        logger.info(f"  -> Severity: {severity} | Action: {transformed.get('action_verb')}")

        # ---------- Severity gating ----------
        post_results = {}

        # X: only CRITICAL + HIGH, max 2 posts/hour (spread across the day)
        X_PER_HOUR_CAP = int(os.environ.get("X_PER_HOUR_CAP", "2"))
        if severity in ("CRITICAL", "HIGH") and transformed.get("x_post"):
            posts_this_hour = _x_posts_last_hour()
            if posts_this_hour >= X_PER_HOUR_CAP:
                logger.info(f"  -> X skipped: hourly cap reached ({posts_this_hour}/{X_PER_HOUR_CAP}). TG+feed still post.")
                log_event("x_post_deferred", threat_id=threat_id, severity=severity,
                          reason=f"hourly_cap {posts_this_hour}/{X_PER_HOUR_CAP}")
            else:
                x_result = post_x(transformed["x_post"], dry_run=dry_run)
                post_results["x"] = x_result
                log_event("x_post", threat_id=threat_id, severity=severity, result=x_result)

        # Telegram: CRITICAL, HIGH, MEDIUM
        if severity in ("CRITICAL", "HIGH", "MEDIUM") and transformed.get("telegram_post"):
            tg_result = post_telegram(transformed["telegram_post"], dry_run=dry_run)
            post_results["telegram"] = tg_result
            log_event("telegram_post", threat_id=threat_id, severity=severity, result=tg_result)

        # Feed: ALL severities
        if config.is_enabled("feed_update"):
            feed_result = feed_append(threat, transformed, threat_id)
            post_results["feed"] = feed_result
            log_event("feed_update", threat_id=threat_id, severity=severity, result=feed_result)

        # Archive
        posted_archive.append(threat, transformed, post_results)
        posted_count += 1
        logger.info(f"  -> Posted to: {[k for k, v in post_results.items() if v.get('posted') or v.get('written')]}")

    # ----------------------------------------------------------
    # 6. CYCLE SUMMARY
    # ----------------------------------------------------------
    duration = time.time() - cycle_start
    summary = {
        "cycle_id": cycle_id,
        "duration_sec": round(duration, 2),
        "threats_collected": len(threats),
        "new_threats": len(new_threats),
        "posted": posted_count,
        "skipped": skipped_count,
        "errors": error_count,
    }
    logger.info(f"[7/9] Cycle summary: {summary}")
    log_event("cycle_summary", **summary)

    # ----------------------------------------------------------
    # 7. STATUS HEARTBEAT
    # ----------------------------------------------------------
    heartbeat(extra={
        **summary,
        "spending": spending_summary(),
        "rate_limits": rate_summary(),
        "circuit_breakers": cb_status(),
    })
    logger.info("[8/9] Heartbeat written")

    logger.info(f"[9/9] === CYCLE END {cycle_id} ({duration:.1f}s) ===\n")
    return summary


# ============================================================
# Entry point
# ============================================================

def main():
    """Main entry point."""
    setup_logging()
    try:
        result = run_cycle()
        sys.exit(0 if result.get("errors", 0) == 0 else 1)
    except SystemExit:
        raise  # pass through halt_if_mismatch exits
    except Exception as e:
        logger.exception(f"FATAL: cycle crashed: {e}")
        log_event("cycle_fatal", error=str(e), error_type=type(e).__name__)
        sys.exit(2)


if __name__ == "__main__":
    main()
