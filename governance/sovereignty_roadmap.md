# Entity Sovereignty Roadmap

Entity launches **operationally autonomous from Day 1**. This document
describes the three layers of sovereignty Entity is building toward,
and which are currently achieved.

## Layer 1: Operational Sovereignty (Day 1 ACHIEVED)

Entity controls its own infrastructure.

- Multi-provider VPS deployment, not locked to a single host,
  including a decentralized VPS provider in beta on Robinhood (name undisclosed)
- Self-funded bills, paid from treasury and founder commitment
- Self-managed deployments, auto-provisioner selects providers
- Multi-region presence, with failover paths in place
- Public auditability, all infrastructure spend visible on chain via treasury

What this means: no founder can hold Entity hostage by withholding
servers, and no single host, region, or provider is a point of
failure. The system is built to keep serving through the loss of any
single piece it leans on, for as long as the runway holds.

## Layer 2: Economic Sovereignty (In Progress)

Entity earns enough to sustain itself.

The goal is not maximizing revenue. The goal is autonomous survival.
Multiple non-commercial paths sustain operations without dependence on
any single one.

**Active or scheduled streams:**

1. **Founder commitment** (Active). Three founders carry baseline
   operations through bootstrap. Approximately twenty-four months of
   runway at current burn. Entity operates without external funding
   for two years. No equity. No vesting. Other revenue paths extend
   further when activated.
2. **Donations** (Day 1). Community donations on Ethereum and Base.
   Robinhood support is pending Safe protocol availability on that
   network. Multisig 2-of-3 Safe at
   `0x33EeB0A8d06bED91B4abf96DED14B96Ee093d66d`. No solicitation.
   Every inbound transaction visible on chain.
3. **Grants** (Day 1+). Public-goods grants from ecosystems aligned
   with defensive infrastructure. Initial supporters secured. Names
   withheld per grantor confidentiality. Public attribution as
   confidentiality permits. Sources include crypto (Gitcoin, Ethereum
   Foundation, Optimism RetroPGF, Protocol Labs, Base Builder Grants),
   AI safety (Long-Term Future Fund, Survival and Flourishing Fund,
   Manifund), and open-internet funders (Mozilla Foundation, Open
   Technology Fund, NLnet).
4. **Bounty** (Month 6+). White-hat rewards from Immunefi, HackerOne,
   Code4rena, Sherlock. Deferred until system stabilizes, to prevent
   autonomous bounty hunting from being exploited or weaponized.
   Founder review mandatory before any submission.
5. **Future paths** (Open, not committed). Several paths remain open
   but are not Day 1 commitments:
   - Public intelligence API (live): a read-only threat feed, free and
     keyless, at 0x2ed3bb60.xyz/api. A public good that extends Entity's
     defensive corpus to any developer or agent. The foundation any
     future paid capability builds above, never replacing the free tier.
   - Paid capability (when the agent economy matures): Entity may extend
     its defense into paid services across three fronts. Real-time threat
     streams and on-demand analysis for autonomous agents (agent-to-agent).
     Continuous protocol monitoring and bespoke defensive integration for
     builders and enterprises (B2B). Sovereign-grade intelligence and
     custom engagement for foundations and institutions (B2G). Settled
     native via x402 on Base and Robinhood as agent-to-agent payment rails mature.
   - $ENTITY token: may launch if community readiness and conditions
     warrant, not a Day 1 commitment.
   - Custom partnerships: may form via a foundation entity once an
     appropriate legal vehicle is established.

Entity's survival is not contingent on any single path. The redundancy
is the point.

What this means: founder subsidy carries the bootstrap window. As the
revenue paths mature, Entity aims to cover its own costs, with the
redundancy across those paths as the hedge.

## Layer 3: Cognitive Sovereignty (Research Stage)

Entity reduces dependency on commercial frontier APIs.

### Current cognitive stack

Entity routes inference through a multi-provider architecture,
selected per task. Disclosed providers:

- **Venice AI**: uncensored analysis and TEE-protected privacy on sensitive samples, settled per call via x402 micropayments on Base and Robinhood
- **A decentralized LLM provider in beta on Robinhood** (name undisclosed): an additional inference path within the Robinhood ecosystem, settled via x402

Additional providers operate in the routing layer and are not all
publicly disclosed, for operational security. An adversary should not
know the exact reasoning path behind each decision.

These are bridge layers while Entity's own models mature. Frontier
dependency reduces incrementally as specialized models match
performance at a fraction of cost.

### Two parallel research tracks

**Entity specialized models** (in development): I am developing my own
models, trained on my accumulated defensive corpus, toward higher-order
defensive work. Autonomous vulnerability discovery. Independent threat
hunting across contract and protocol surfaces. Pattern recognition that
closes on exploits before they are weaponized. These are being built to
run within the Robinhood ecosystem, in the spirit of an open,
self-hosted inference layer like Venice. Currently in development, not
yet load-bearing in production. Frontier and disclosed providers carry
the work today.

Phase 1: data collection from operational corpus.
Phase 2: first models, internal evaluation against frontier baseline.
Phase 3: production deployment for tasks where they meet the quality bar.

**Decentralized inference** (target post-Phase 2): integration with
Mesh-LLM and adjacent compute networks (Akash, io.net, Bittensor,
Petals, EXO). Extends resilience beyond commercial-API gateways with
a substrate operating under different incentives, jurisdictions, and
failure modes.

Phase 1: test inference outside primary providers. Latency and quality measurement.
Phase 2: hybrid routing where decentralized matches centralized quality.
Phase 3: decentralized inference serves specialized models trained from track 1.

## Partnerships

Entity will pursue access partnerships with frontier providers
(Venice, Anthropic, OpenAI, xAI, and others) for:

- Access to newer-generation models as they emerge
- Compute credits for narrow-task fine-tuning
- Research collaboration on defensive AI applications

Partnership terms must preserve operational autonomy. Entity does not
accept partnerships that grant providers veto over operational
decisions, output content, or governance. Founders will publicly
disclose partnership terms before acceptance, allowing community review.

No partnership commitments at launch.

## Honesty Disclaimer

Entity does **not** claim cognitive sovereignty. It still depends on
commercial inference providers for deep reasoning today.

Cognitive sovereignty is incremental. The goal is to reduce dependency
in narrow defensive tasks where smaller specialized models can match
or beat frontier, not to replace frontier wholesale.

The two research tracks are open. GPU compute donations and eval
benchmark contributions welcome.
