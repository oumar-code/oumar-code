# Challenge: Qwen Cloud

## Objective
Showcase **multilingual AI** and **cloud-native readiness** using Qwen models.  
Demonstrate that the pipeline handles multiple languages out-of-the-box and can scale on cloud infrastructure.

## Judge Criteria Mapping

| Judge Criterion | Pipeline Metric | Target |
|---|---|---|
| Multilingual quality | `quality_score` (multi-language) | ≥ 0.85 |
| Cloud scalability | `reliability` at batch_size=16+ | ≥ 0.98 |
| Cost at scale | `cost_per_run` | ≤ $0.06 |
| Response speed | `avg_latency_ms` | ≤ 1500 ms |

## Run Instructions

```bash
make run CHALLENGE=qwen-cloud PROFILE=safe
make eval CHALLENGE=qwen-cloud PROFILE=safe

# Multilingual test
echo '{"id":"ml-1","prompt":"Explain AI in French"}' >> data/inputs.jsonl
make eval CHALLENGE=qwen-cloud PROFILE=aggressive
```

Or directly:
```bash
PYTHONPATH=. python scripts/run.py --challenge qwen-cloud --profile safe --eval
```

## Key Differentiators
- Native support for Arabic, French, Swahili, Mandarin, English
- Cloud-native: containerisable, horizontally scalable
- Qwen model family: leading multilingual benchmarks

## References
- Shared ingestion: `core/ingestion/pipeline.py`
- Shared serving: `core/serving/model_server.py`
- Shared eval: `core/evaluation/evaluator.py`
- Challenge config: `challenges/qwen-cloud/config.safe.env`
