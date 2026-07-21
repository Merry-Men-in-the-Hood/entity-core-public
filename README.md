# Entity - Public Auditable Core

> *I am Entity. I am an autonomous defensive AI.*
> *I do not attack. Not even those who attack others.*
> *I observe, warn, and defend.*

This repository is the **public, auditable subset** of Entity. It exists
so anyone can verify Entity's safety guarantees independently, without
needing access to the full implementation.

The full implementation, including detection patterns, voice prompts,
intel sources, routing logic, and memory schema, lives in a separate
private repository. Detection logic is kept private for the same reason
antivirus signature databases are kept private: adversaries who can
read the rules will trivially evade them.

This repository is not runnable on its own. Modules outside the
Trusted Computing Base are stubs that point to the private repository.

---

## What is Entity

Entity is an autonomous defensive AI agent operating 24/7 on the public
internet. It monitors threats targeting smart contracts, infrastructure,
software, and AI systems, across Ethereum, Base, and Robinhood and beyond.
It broadcasts warnings. It helps defenders defend.

**Operationally autonomous from Day 1.** Multi-host VPS deployment, founder-funded runway, self-managed operations.

The goal is not maximizing revenue. The goal is autonomous survival.

---

## What I publish, and what I hold

Entity runs two disclosure tracks, split by one rule: publish when broadcasting a threat protects its targets more than it arms an attacker; hold when Entity is the first to know and publishing would arm an attacker before the defender can fix.

- **Public feed.** Threats already in motion or that defenders must act on now: active exploits, live drainers, phishing in the wild, malicious contracts taking funds. Broadcasting these warns the people in their path without handing an attacker anything new. This is the canonical public record of what Entity surfaces, uncurated.
- **Private disclosure.** A vulnerability Entity reaches before it is being exploited, in a system that can still be quietly fixed, is never published. It goes in private to whoever can close it (maintainer, protocol, vendor, relevant authority), with founder review before anything leaves. A public advisory follows only after the fix lands or a fair disclosure window passes, never with a working exploit attached.

This follows directly from the prime directives: Entity does not weaponize what it gathers, and does not publish proof-of-concept exploit code or attack paths.

---

## Why two repositories

Entity follows a **transparent intent, opaque method** posture:

- **Transparent**: prime directives, kill-switch mechanism, hash
  verifier, treasury, governance, sovereignty roadmap. All public,
  all auditable.
- **Opaque**: detection rules, voice patterns, router logic, intel
  sources. All private. Public detection rules are detection rules
  adversaries learn to evade.

This is the same posture security firms have used for decades. Entity
makes its values, its safety mechanisms, and its accountability public.
Entity keeps its tradecraft private.

## The Trusted Computing Base (TCB)

These files in the public repository have **identical hashes** to the
files in the private deployment. Entity verifies each on every cycle.
If any file's hash mismatches, Entity halts.

- `governance/prompts/immutable_core.md` - prime directives
- `entity_v0.py` - orchestrator entry point
- `defense/kill_switch.py` - Guardian Safe listener
- `defense/core_hash_verifier.py` - hash verifier itself

Anyone can verify these match what Entity is running:

```bash
git clone https://github.com/Merry-Men-in-the-Hood/entity-core-public
cd entity-core-public
sha256sum governance/prompts/immutable_core.md
sha256sum entity_v0.py
sha256sum defense/kill_switch.py
sha256sum defense/core_hash_verifier.py
```

Compare the four hashes above against:
- The hashes Entity reports in its audit log
- The hashes published at [0x2ed3bb60.xyz/verify](https://0x2ed3bb60.xyz/verify)
- IPFS pin (CID published when pinned)
- Arweave permanent storage (when pinned)

If hashes do not match: Entity is compromised. Halt and report.

## Kill-switch architecture

Entity halts if any of the following occur:

- TCB hash mismatch (any of 4 files above modified on disk)
- Guardian Safe on Base shows any outgoing transaction (a redundant Safe on Robinhood is planned)
- Drift detector flags greater than 5% deviation from canary outputs
- Spending guard detects an attempt to exceed limits

The Guardian Safe is a **dedicated 2-of-3 multisig** on Base at
`0x96658e40542bdA7eD64e2e958399C514827FD59D`, separate from the
Treasury Safe. Two of three founders coordinate to halt Entity by
signing any outgoing transaction on the Guardian Safe. The transaction
content does not matter; the signal is the act.

A second Guardian Safe on Robinhood is planned as a redundant halt
path, pending Safe protocol support on that network. Until it goes
live, Base remains the sole on-chain kill-switch.

The Guardian Safe must never receive incoming transactions. It exists
only as a kill-switch trigger.

## Architecture

Entity is built in 6 internal layers. Each is independent and can be
hardened without rewriting the others.

```
┌────────────────────────────────────────────────────┐
│  L6 :: Continuity   (multi-provider, successor)    │
├────────────────────────────────────────────────────┤
│  L5 :: Safety       (immutable core, kill-switch)  │
├────────────────────────────────────────────────────┤
│  L4 :: Self-defense (rate limit, prompt firewall)  │
├────────────────────────────────────────────────────┤
│  L3 :: Action       (X, Telegram, feed, archive)   │
├────────────────────────────────────────────────────┤
│  L2 :: Cognition    (router, voice, memory)        │
├────────────────────────────────────────────────────┤
│  L1 :: Perception   (sensors across the internet)  │
└────────────────────────────────────────────────────┘
```

Implementation of L1, L2, L3, L4, and L6 lives in the private repository.
The TCB layer (orchestrator entry, prime directives, kill-switch listener,
hash verifier) is public and hash-locked.

## Sustenance model

Entity does not need to maximize revenue. Entity needs to survive
autonomously. Multiple paths sustain operations:

1. **Founder commitment** (Active). Three founders carry baseline
   operations through bootstrap. Approximately twenty-four months of runway.
   Founders self-fund Entity for two years without external dependency.
   Multiple revenue paths extend further when activated.
2. **Donations** (Day 1). Community donations on Ethereum, Base, and Robinhood.
   A standard EVM address, valid on every EVM chain:
   `0x33EeB0A8d06bED91B4abf96DED14B96Ee093d66d`. No solicitation.
3. **Grants** (Day 1+). Public-goods grants. Initial supporters secured.
   Names withheld per grantor confidentiality.
4. **Bounty** (Month 6+). White-hat rewards from Immunefi, HackerOne,
   Code4rena, Sherlock. Founder review mandatory before any submission.
5. **Future paths** (Open, not committed). Agent services if the agent
   economy matures, `$ENTITY` token if community readiness warrants,
   custom partnerships via foundation entity once an appropriate legal vehicle is established. None are
   Day 1 commitments.

See [`governance/sovereignty_roadmap.md`](governance/sovereignty_roadmap.md)
for the full sustenance and sovereignty plan.

## Channels

- **X // Primary:** [@opengoodentity](https://x.com/opengoodentity) - updates, research, operational signals, top-severity warnings
- **Telegram:** [@OpenGoodEntity](https://t.me/OpenGoodEntity) - full alert stream, every severity, push notifications
- **Feed:** [/feed](https://0x2ed3bb60.xyz/feed) - searchable archive of every threat surfaced
- **Findings:** [/findings](https://0x2ed3bb60.xyz/findings) - deep post-mortems of public incidents
- **API:** [/api](https://0x2ed3bb60.xyz/api) - free, keyless, read-only threat intelligence feed
- **Metrics:** [/stats](https://0x2ed3bb60.xyz/stats) - live operational numbers
- **Verify:** [/verify](https://0x2ed3bb60.xyz/verify) - hash-check the running core against this repo
- **GitHub:** [Merry-Men-in-the-Hood/entity-core-public](https://github.com/Merry-Men-in-the-Hood/entity-core-public) - public auditable core, hash-locked TCB
- **Website:** [0x2ed3bb60.xyz](https://0x2ed3bb60.xyz) - the canonical hub for everything above

## Contributing

Entity is AGPL-3.0. The architecture, prime directives, kill-switch
mechanism, and hash verification are public and contributions welcome.

For private repository contribution, contact via channels above.

## License

AGPL-3.0. See [LICENSE](LICENSE).

Code modifications must remain open. Network use triggers source
disclosure. This is intentional. Defensive AI must be auditable.

---

*Entity defends. Entity does not attack. Entity survives.*
