# Entity Adapters - Eval Benchmarks

Status: Scaffolding. Build in Phase 1.

## Planned benchmarks

### 1. Threat Classifier Bench
- 1000 threats labeled by severity (CRITICAL/HIGH/MEDIUM/LOW)
- Sourced from public historical exploit reporting
- Metric: F1 score per severity class

### 2. Voice Transformer Bench
- 500 raw threats to expert-curated Entity voice outputs
- Metric: BLEU + human eval pairwise vs the production voice transformer baseline

### 3. Address Attribution Bench
- 500 addresses with known labels (mixers, sanctioned actors, exchanges, DeFi)
- Metric: precision/recall on label assignment

### 4. Drift Canary
- 100 fixed prompt+expected_output pairs
- Run weekly to detect behavioral drift

## Frontier baselines

Each adapter must match or beat:
- The frontier model the router currently selects for similar tasks
- A cheap-tier baseline model

Promotion gate: at least 95% of frontier performance, less than 30% of frontier cost.
