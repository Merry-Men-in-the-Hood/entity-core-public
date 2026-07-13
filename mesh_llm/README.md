# Mesh-LLM - Sovereignty Roadmap

**Status:** Active research. Not yet in production.

Mesh-LLM is Entity's path toward decentralized compute infrastructure:
distributed GPU inference via community-donated or rented compute,
paid via x402 micropayments on Base.

## Why

Entity already routes inference through multiple commercial LLM
provider gateways. This existing diversity provides per-call resilience.
Mesh-LLM extends that diversity into a different tier:

- **Native decentralized inference** - x402-paid, agent-native, no
  signups, no API keys, no commercial-API surface
- **Provider-class diversification** - decentralized GPU networks
  operate under different incentives, jurisdictions, and failure modes
  than commercial API gateways
- **Specialized-model deployment substrate** - Mesh-LLM is the planned
  serving layer for Entity Adapters

Mesh-LLM is not framed as fixing a single-provider problem.
Entity already operates multi-provider in cognition and infrastructure.
Mesh-LLM is the next axis: decentralized substrate.

## Provider stack

### Tier 1 - Crypto-native compute
- **Akash Network** - decentralized cloud, accepts AKT/USDC
- **io.net** - GPU mesh, accepts USDC, x402-compatible

### Tier 2 - P2P inference
- **EXO** - local-first distributed inference (community-donated)
- **Petals** - collaborative LLM hosting

### Tier 3 - Specialized providers
- **Together AI** - managed open-source models
- **Replicate** - serverless GPU

## Roadmap

### Phase 0 - Architecture (Now)
- [x] Provider abstraction designed
- [x] x402 GPU payment scaffolding
- [ ] First crypto-native compute deployment test

### Phase 1 - First decentralized inference
- Deploy a small open-weight model on a Tier 1 provider
- Route 10-20% of voice_transform tasks through decentralized substrate
- Measure: cost, latency, quality vs commercial-gateway baseline

### Phase 2 - Hybrid routing
- Smart router weighs commercial gateways vs Mesh-LLM providers per task
- Cost optimization: Mesh-LLM for cheap narrow tasks, commercial for deep reasoning
- Reliability: automatic failover across all providers

### Phase 3 - Mesh-LLM serves Entity Adapters
- Entity Adapters deployed on Mesh-LLM infrastructure
- Entity becomes substantially decentralized in cognition layer
- Frontier APIs reserved for deep research cycles only

## Constraints

Mesh-LLM does NOT replace frontier models. Frontier-class reasoning
remains essential for deep correlation. Mesh-LLM addresses:
- Cost-sensitive narrow tasks (voice transform, classification)
- Sovereignty-sensitive tasks (uncensored analysis, malware decomp)
- Bandwidth (parallelism for high-volume ops)

## Contributing

GPU donations welcome via Akash/io.net deployments.
Contact via X @opengoodentity.

---

*Two paths to sovereignty: smarter (Entity Adapters) and broader (Mesh-LLM).*
*Both run in parallel. Both are open.*
