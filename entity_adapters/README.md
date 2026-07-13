# Entity Adapters - Research Roadmap

**Status:** Active research. Not yet in production.

Entity Adapters is Entity's path toward specialized cognitive sovereignty
via fine-tuned LoRA adapters trained on defensive task corpora.

## Why

Frontier models are brilliant but:
- **Not specialized** for cybersecurity defense
- **Aligned for refusal** - sometimes refuse legitimate analysis (malware samples, exploit code, adversarial content)
- **Cost-sensitive at scale** - frontier inference costs add up fast for high-volume narrow tasks
- **Dependent on commercial APIs** - single point of failure

Entity Adapters fine-tunes small open-weight base models with LoRA adapters
on Entity's accumulated threat corpus to:

1. Specialize for narrow defensive tasks (faster, cheaper, more accurate)
2. Reduce dependency on commercial frontier APIs
3. Run uncensored where necessary (malware analysis, exploit decompilation)
4. Become deployable on community Mesh-LLM infrastructure

## Roadmap

### Phase 0 - Research baseline (Now)
- [x] Architecture design
- [x] Threat data schema
- [ ] Identify candidate base models (open-weight, 7-9B parameter range)

### Phase 1 - Data collection
- Accumulate 1000+ documented threats with Entity's analysis
- Build training corpus from Entity's audit logs + posted archive
- Curate eval benchmark from historical exploit dataset

### Phase 2 - First adapters
- Fine-tune LoRA adapters for narrow tasks:
  - `threat_classifier` - severity + category prediction
  - `voice_transformer` - replace the production voice transformer for cheap narrow tasks
  - `address_attribution` - wallet labeling
- Acquire GPU compute via grants or community Mesh-LLM
- Eval against frontier baseline

### Phase 3 - Production deployment
- Adapters serve narrow tasks via Mesh-LLM
- Frontier APIs reserved for deep reasoning + complex synthesis
- Cost reduction target: 60-80% on narrow tasks

### Phase 4 - Continuous self-improvement
- Adapters retrained periodically on new Entity data
- Drift monitoring + canary eval gates promotion
- Community-contributed eval benchmarks

## Why "Entity Adapters"?

The name is literal: these are fine-tuned LoRA adapters, trained on
Entity's own defensive corpus, that specialize frontier base models for
narrow defensive tasks. The project name is descriptive, not a codename.

## Contributing

This research is open. Contributions welcome:

- Eval benchmark contributions
- Architecture proposals
- Compute donations (via Mesh-LLM)
- Training pipeline improvements

GitHub: `github.com/Merry-Men-in-the-Hood/entity-adapters` (forthcoming)

---

*Sovereignty is incremental. Entity Adapters is one path. Mesh-LLM is another.*
*Honest about dependency is itself a defensive posture.*
