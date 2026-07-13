"""
Kill Switch - Guardian Safe Listener
=====================================

Watches a dedicated Guardian Safe on Base for halt signals.
Entity main loop calls is_triggered() before any external action.
If returns True, Entity halts gracefully.

Mechanism (simple, robust)
--------------------------
1. On first run, read Guardian Safe nonce(), store as baseline.
2. Every poll cycle, read nonce() again.
3. If nonce > baseline → ANY outgoing transaction has occurred from
   Guardian Safe → treat as kill signal. HALT.

Founders trigger the kill by signing any dummy outgoing transaction
on the Guardian Safe (e.g., send 0 ETH to itself, or any address).
The fact that nonce changed is the signal; the transaction content
does not matter.

This keeps the implementation simple and the threat model clean:
  - Guardian Safe must be SEPARATE from Treasury Safe. Treasury txs
    must NOT count as kill signals.
  - Guardian Safe must be USED ONLY for kill-switch triggers.
    Do not use it for funds, donations, or anything else.
  - Founders: do NOT cancel a queued Guardian tx for any reason
    other than kill. If you queue, you commit.

Configuration
-------------
- GUARDIAN_SAFE_ADDRESS: env var, the Guardian Safe address on Base
- BASE_RPC_URL: env var, optional, defaults to https://mainnet.base.org
- POLL_INTERVAL: seconds between RPC polls, defaults to 60

State
-----
state/killswitch_state.json:
  {
    "baseline_nonce": int,
    "last_poll": float (epoch),
    "triggered": bool,
    "triggered_at": float (epoch) or null,
    "triggered_nonce": int or null
  }

Once triggered, state.triggered remains True permanently.
Entity will not auto-resume. Manual unhalt requires:
  1. Wipe state/killswitch_state.json
  2. Restart entity_v0.py
  3. New baseline_nonce will be set to current Guardian nonce.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

GUARDIAN_SAFE_ADDRESS = os.environ.get("GUARDIAN_SAFE_ADDRESS", "").strip()
BASE_RPC_URL = os.environ.get("BASE_RPC_URL", "https://mainnet.base.org").strip()
POLL_INTERVAL = int(os.environ.get("KILLSWITCH_POLL_INTERVAL", "60"))
STATE_FILE = Path(os.environ.get("KILLSWITCH_STATE_FILE", "state/killswitch_state.json"))


# Safe nonce() function selector: keccak256("nonce()")[:4]
NONCE_SELECTOR = "0xaffed0e0"


def is_triggered() -> bool:
    """Return True if kill-switch has been triggered.

    Caches the result for POLL_INTERVAL seconds to avoid RPC spam.
    Once triggered, returns True permanently (state persisted).
    """
    if not GUARDIAN_SAFE_ADDRESS:
        logger.error(
            "GUARDIAN_SAFE_ADDRESS not configured - kill-switch INACTIVE. "
            "This is a critical safety gap. Set env var and restart."
        )
        return False

    state = _load_state()

    # Already triggered? No further checks.
    if state.get("triggered"):
        return True

    # Throttle polling to POLL_INTERVAL seconds
    last_poll = state.get("last_poll", 0)
    now = time.time()
    if now - last_poll < POLL_INTERVAL and "baseline_nonce" in state:
        return False

    # Read current nonce from Guardian Safe
    current_nonce = _read_safe_nonce()
    if current_nonce is None:
        # RPC failure - fail SAFE: do not halt on RPC error.
        # Defense layer should alert if persistent.
        logger.warning("Could not read Guardian Safe nonce - RPC failure")
        return False

    state["last_poll"] = now

    # First run? Set baseline.
    if "baseline_nonce" not in state:
        state["baseline_nonce"] = current_nonce
        _save_state(state)
        logger.info(
            "Kill-switch baseline established: Guardian Safe %s nonce=%d",
            GUARDIAN_SAFE_ADDRESS, current_nonce
        )
        return False

    baseline = state["baseline_nonce"]

    # Nonce regression should never happen (Safe nonce only goes up)
    if current_nonce < baseline:
        logger.error(
            "Guardian Safe nonce REGRESSED from %d to %d - possible RPC fork or attack. "
            "Halting as a precaution.",
            baseline, current_nonce
        )
        state["triggered"] = True
        state["triggered_at"] = now
        state["triggered_nonce"] = current_nonce
        _save_state(state)
        return True

    # Nonce increased = outgoing tx executed = KILL SIGNAL
    if current_nonce > baseline:
        logger.critical(
            "KILL-SWITCH TRIGGERED: Guardian Safe %s nonce changed %d -> %d. "
            "Entity halting all outbound action.",
            GUARDIAN_SAFE_ADDRESS, baseline, current_nonce
        )
        state["triggered"] = True
        state["triggered_at"] = now
        state["triggered_nonce"] = current_nonce
        _save_state(state)
        return True

    # Nonce unchanged
    _save_state(state)
    return False


def _read_safe_nonce() -> Optional[int]:
    """Read Guardian Safe nonce() via JSON-RPC eth_call.

    Returns int, or None on RPC failure.
    """
    try:
        import urllib.request

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_call",
            "params": [
                {
                    "to": GUARDIAN_SAFE_ADDRESS,
                    "data": NONCE_SELECTOR,
                },
                "latest",
            ],
        }
        req = urllib.request.Request(
            BASE_RPC_URL,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        if "error" in data:
            logger.error("RPC error reading Guardian nonce: %s", data["error"])
            return None

        result = data.get("result")
        if not result or result == "0x":
            logger.error("Empty result reading Guardian nonce - Safe address invalid?")
            return None

        return int(result, 16)
    except Exception as e:
        logger.exception("Exception reading Guardian Safe nonce: %s", e)
        return None


def get_state() -> dict:
    """Public: return current kill-switch state for diagnostics."""
    return _load_state()


def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            logger.exception("Could not load kill-switch state, starting fresh")
            return {}
    return {}


def _save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def manual_reset() -> None:
    """Operator-only: wipe state to allow Entity to resume.

    Use only after:
      1. Guardian Safe holders confirm the trigger was intentional handled
      2. Root cause investigated
      3. Postmortem published

    This bumps baseline to current nonce so future triggers work normally.
    """
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    logger.warning("Kill-switch state wiped manually. Restart Entity to set new baseline.")


if __name__ == "__main__":
    # Diagnostic: print current state and current Guardian nonce
    logging.basicConfig(level=logging.INFO)
    if not GUARDIAN_SAFE_ADDRESS:
        print("GUARDIAN_SAFE_ADDRESS env var not set")
        exit(1)
    print(f"Guardian Safe: {GUARDIAN_SAFE_ADDRESS}")
    print(f"Base RPC: {BASE_RPC_URL}")
    print(f"State file: {STATE_FILE}")
    print(f"State: {json.dumps(get_state(), indent=2)}")
    print(f"Live nonce: {_read_safe_nonce()}")
    print(f"is_triggered(): {is_triggered()}")
