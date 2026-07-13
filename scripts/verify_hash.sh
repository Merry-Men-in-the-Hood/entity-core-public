#!/bin/bash
# Entity - Verify TCB file hashes against published baseline
# Public verification utility. Run from anywhere with a clone of this repo.
#
# Usage:
#   ./scripts/verify_hash.sh
#
# Prints SHA256 hashes for the four Trusted Computing Base files.
# Compare against the hashes Entity publishes at:
#   - https://0x2ed3bb60.xyz/verify
#   - Entity audit log
#   - IPFS pin (CID published when pinned)
#   - Arweave permanent storage (when pinned)

set -e

# Locate repo root (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

TCB_FILES=(
    "governance/prompts/immutable_core.md"
    "entity_v0.py"
    "defense/kill_switch.py"
    "defense/core_hash_verifier.py"
)

echo "=== Entity TCB hashes (SHA256) ==="
echo ""
for f in "${TCB_FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "MISSING  $f"
        continue
    fi
    HASH=$(sha256sum "$f" | awk '{print $1}')
    echo "$HASH  $f"
done

echo ""
echo "Compare these against hashes published at https://0x2ed3bb60.xyz/verify"
echo "If any mismatch, Entity is compromised. Halt and report."
