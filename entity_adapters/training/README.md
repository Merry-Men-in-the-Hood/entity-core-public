# Entity Adapters - Training Pipeline

Status: Scaffold. Active in Phase 2.

## Pipeline (planned)

1. **Data extraction**: pull Entity's posted_archive + audit_log to training samples
2. **Curation**: filter low-quality, dedupe, balance severities
3. **Format**: convert to standard instruction-tuning format with Entity voice
4. **Fine-tune**: LoRA on base model (rank 16-64, alpha 32, target attn+ffn)
5. **Eval**: against benchmarks/canary outputs
6. **Promote**: gate by drift_detector + human review

## Compute requirements

- Base 7-8B model, LoRA rank 16: ~24GB VRAM (consumer high-end / single workstation GPU)
- Larger model, LoRA rank 32: ~32GB VRAM (datacenter accelerator class)
- Training time: 2-8 hours per adapter

## Funding paths

- Frontier-provider research credit programs
- AI safety grants (Open Phil, Long-Term Future Fund)
- Mesh-LLM community compute donations
