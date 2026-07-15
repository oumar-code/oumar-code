# Challenge: Arm Create

## Objective
Demonstrate compute-efficient AI inference optimised for Arm-based hardware (cloud or edge).  
The core goal is to maximise **throughput-per-watt** using the shared pipeline while minimising cost.

## Judge Criteria Mapping

| Judge Criterion | Pipeline Metric | Target |
|---|---|---|
| Performance efficiency | `avg_latency_ms` | ≤ 800 ms |
| Cost optimisation | `cost_per_run` | ≤ $0.05 |
| Reliability | `reliability` | ≥ 0.98 |
| Quality | `quality_score` | ≥ 0.85 |

## Run Instructions

```bash
# Safe profile (recommended for live demo)
make run CHALLENGE=arm-create PROFILE=safe

# Aggressive profile (higher throughput, higher risk)
make run CHALLENGE=arm-create PROFILE=aggressive

# Full evaluation
make eval CHALLENGE=arm-create PROFILE=safe
```

Or directly:
```bash
PYTHONPATH=. python scripts/run.py --challenge arm-create --profile safe --eval
```

## Key Differentiators
- Model: lightweight quantised variant (INT8 / Q4) preferred
- Batch inference to amortise startup cost
- Target: Arm Neoverse N2 or equivalent cloud instance

## References
- Shared ingestion: `core/ingestion/pipeline.py`
- Shared serving: `core/serving/model_server.py`
- Shared eval: `core/evaluation/evaluator.py`
- Challenge config: `challenges/arm-create/config.safe.env`
