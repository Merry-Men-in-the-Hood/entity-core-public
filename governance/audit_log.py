"""
Audit Log for Entity v0
========================

Append-only JSONL log of every significant decision Entity makes.

Used for:
- Transparency (anyone can review Entity's reasoning history)
- Debugging (incident response, drift detection)
- Postmortems (when something goes wrong)
- Grant applications (proof of activity)

Format: one JSON object per line.

Local file at logs/audit.jsonl is the primary store.
Daily summaries pinned to IPFS for long-term permanence (rolled out post-stabilization).
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import config

logger = logging.getLogger(__name__)


def log_event(event_type: str, **kwargs: Any) -> None:
    """
    Append an audit log entry.

    :param event_type: e.g., "cycle_start", "threat_observed", "post_published",
                       "post_skipped", "halt", "spend_blocked", etc.
    :param kwargs: arbitrary metadata
    """
    if not config.is_enabled("audit_log"):
        return

    entry = {
        "ts": time.time(),
        "iso_time": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "entity_version": config.ENTITY_VERSION,
        **kwargs,
    }

    try:
        path = config.PATHS["audit_log"]
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
    except IOError as e:
        logger.error(f"Failed to write audit log: {e}")


def tail(n: int = 50) -> list[dict]:
    """Return last N audit log entries."""
    path = config.PATHS["audit_log"]
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        entries = []
        for line in lines[-n:]:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries
    except IOError:
        return []
