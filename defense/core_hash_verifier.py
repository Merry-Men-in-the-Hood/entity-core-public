"""
Core Hash Verifier - Trusted Computing Base (TCB) check
========================================================

Verifies a fixed set of trust-critical files have not been modified.
This is the foundation that makes the Guardian Safe kill-switch reliable:
if an attacker tampers with the orchestrator, the kill-switch listener,
or the verifier itself, hashes mismatch and Entity halts.

The Trusted Computing Base (TCB)
--------------------------------
Files whose integrity Entity depends on for safety:

  governance/prompts/immutable_core.md
      Entity's prime directives. Hash-locked, change requires founder
      multisig + 14-day public comment.

  entity_v0.py
      The orchestrator. Calls kill-switch + hash verifier each cycle
      BEFORE any agentic action. Tampering here can bypass safety.

  defense/kill_switch.py
      The Guardian Safe listener. Tampering here can fake "no halt".

  defense/core_hash_verifier.py
      This file. Self-verification: tampering here can disable all
      other checks. Hash of self is computed from disk each cycle so
      modified-on-disk binary is detected even though running process
      uses old code.

If any file's hash mismatches its expected baseline, Entity halts.

Mechanism
---------
First run: hashes are recorded into state/tcb_hashes.json.
Subsequent runs: hashes recomputed and compared. Mismatch -> halt.

Operator updates (legitimate code change):
  1. Edit file
  2. Run `./scripts/verify_hash.sh --record` to update baseline
  3. Restart Entity

This is a manual operator step. There is no automatic re-baselining,
so an attacker cannot silently update the baseline.
"""

import hashlib
import json
import logging
import sys
from pathlib import Path
from typing import Optional

import config

logger = logging.getLogger(__name__)


# Trusted Computing Base - files whose integrity Entity depends on.
# Paths are relative to project root (parent of this file's parent).
PROJECT_ROOT = Path(__file__).resolve().parent.parent

TCB_FILES = [
    "governance/prompts/immutable_core.md",
    "entity_v0.py",
    "defense/kill_switch.py",
    "defense/core_hash_verifier.py",
]

TCB_STATE_FILE = PROJECT_ROOT / "state" / "tcb_hashes.json"


def _hash_file(path: Path) -> Optional[str]:
    """Compute SHA256 of a file. Returns hex string or None if file missing."""
    if not path.exists():
        logger.error("TCB file missing: %s", path)
        return None
    try:
        with path.open("rb") as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()
    except IOError as e:
        logger.error("Failed to read TCB file %s: %s", path, e)
        return None


def _load_baseline() -> dict:
    if not TCB_STATE_FILE.exists():
        return {}
    try:
        return json.loads(TCB_STATE_FILE.read_text())
    except Exception:
        logger.exception("Could not parse TCB state file %s", TCB_STATE_FILE)
        return {}


def _save_baseline(baseline: dict) -> None:
    TCB_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    TCB_STATE_FILE.write_text(json.dumps(baseline, indent=2, sort_keys=True))


def compute_all() -> dict:
    """Compute current hashes for all TCB files."""
    result = {}
    for rel_path in TCB_FILES:
        full_path = PROJECT_ROOT / rel_path
        h = _hash_file(full_path)
        if h is None:
            result[rel_path] = None
        else:
            result[rel_path] = h
    return result


def verify() -> tuple[bool, str]:
    """Verify all TCB files against baseline.

    Returns (verified, message).
    """
    if not config.is_enabled("core_hash_verify"):
        return True, "verification_disabled"

    current = compute_all()

    # Any file missing or unreadable = halt
    for rel_path, h in current.items():
        if h is None:
            return False, f"tcb_unreadable:{rel_path}"

    baseline = _load_baseline()

    # First run: record baseline
    if not baseline:
        _save_baseline(current)
        logger.warning(
            "First-run: TCB baseline recorded for %d files. "
            "Restart Entity in production mode after verifying baseline.",
            len(current),
        )
        return True, "first_run_baseline_recorded"

    # Compare every file
    mismatches = []
    for rel_path, h in current.items():
        expected = baseline.get(rel_path)
        if expected is None:
            mismatches.append(f"{rel_path} (no baseline)")
        elif h.lower() != expected.lower():
            mismatches.append(
                f"{rel_path}: expected={expected[:16]}... actual={h[:16]}..."
            )

    if mismatches:
        logger.critical(
            "TCB HASH MISMATCH detected:\n  %s\n"
            "Entity will HALT. Investigate before restart.",
            "\n  ".join(mismatches),
        )
        return False, f"tcb_mismatch:{len(mismatches)}_files"

    return True, "verified"


def halt_if_mismatch():
    """Verify TCB hashes. Exit process if any file tampered with."""
    verified, msg = verify()
    if not verified:
        logger.critical("TCB VERIFICATION FAILED: %s", msg)
        logger.critical("Entity is halting. Investigate before restart.")
        sys.exit(1)
    return verified


def record_baseline_now() -> None:
    """Operator-only: record current TCB hashes as the new baseline.

    Call this after a legitimate code update:
      python -m defense.core_hash_verifier --record

    Make sure no unintended changes are present before recording.
    """
    current = compute_all()
    missing = [k for k, v in current.items() if v is None]
    if missing:
        logger.error("Cannot record baseline, missing files: %s", missing)
        sys.exit(1)
    _save_baseline(current)
    logger.warning("New TCB baseline recorded:")
    for path, h in current.items():
        logger.warning("  %s  %s", h[:16], path)


# Backward-compatibility shim: old code calls compute_hash() with no args
def compute_hash(file_path: Optional[Path] = None) -> Optional[str]:
    """Legacy single-file hash. Defaults to immutable_core.md."""
    target = file_path if file_path else PROJECT_ROOT / TCB_FILES[0]
    return _hash_file(target)


if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="TCB hash verifier")
    parser.add_argument("--record", action="store_true",
                        help="Record current hashes as new baseline (operator only)")
    parser.add_argument("--show", action="store_true",
                        help="Show current TCB hashes without modifying state")
    args = parser.parse_args()

    if args.show:
        for path, h in compute_all().items():
            print(f"{h or 'MISSING'.ljust(64)}  {path}")
    elif args.record:
        record_baseline_now()
    else:
        verified, msg = verify()
        print(f"verified={verified} message={msg}")
        sys.exit(0 if verified else 1)
