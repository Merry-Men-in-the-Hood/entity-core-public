"""
Configuration - STUB for public repository

The full configuration (thresholds, feature flags, paths) lives in the
private repository at github.com/Merry-Men-in-the-Hood/entity-core-private.

This stub exists so that public-repo browsing of entity_v0.py and
defense modules does not produce confusing import errors. Running
Entity from the public repo alone will fail; that is intentional.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
IMMUTABLE_CORE_PATH = PROJECT_ROOT / "governance/prompts/immutable_core.md"
IMMUTABLE_CORE_HASH_EXPECTED = ""
ENTITY_VERSION = "0.0-stub"

MAX_THREATS_PER_CYCLE = 0  # private impl sets the real value

PATHS = {
    "core_hash":   PROJECT_ROOT / "state/core_hash.txt",
    "tcb_hashes":  PROJECT_ROOT / "state/tcb_hashes.json",
    "audit_log":   PROJECT_ROOT / "logs/audit.jsonl",
    "entity_log":  PROJECT_ROOT / "logs/entity.log",
}


def is_enabled(feature: str) -> bool:
    """Stub: nothing enabled in public-repo configuration."""
    return False


def env_check() -> dict:
    """Stub: empty env dict."""
    return {}


# Module-level guard: warn anyone running this from public repo
if __name__ == "__main__":
    raise NotImplementedError(
        "Public repository contains TCB files only for hash verification. "
        "To run Entity, clone github.com/Merry-Men-in-the-Hood/entity-core-private."
    )
