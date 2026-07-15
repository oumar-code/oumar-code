# Challenge: Backblaze Genblaze

## Objective
Build an end-to-end **media workflow pipeline** that ingests, processes, and stores assets via Backblaze B2.  
Use the shared LLM serving layer to add AI-generated metadata, captions, or summaries to media objects stored in B2.

## Judge Criteria Mapping

| Judge Criterion | Pipeline Metric | Target |
|---|---|---|
| B2 integration depth | reliability of B2 upload/download | ≥ 0.99 |
| Pipeline throughput | `avg_latency_ms` (end-to-end) | ≤ 3000 ms |
| Cost efficiency | `cost_per_run` | ≤ $0.08 |
| Output quality | `quality_score` (metadata accuracy) | ≥ 0.80 |

## Run Instructions

```bash
# Requires B2_APPLICATION_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET_NAME in .env

make run CHALLENGE=backblaze-genblaze PROFILE=safe
make eval CHALLENGE=backblaze-genblaze PROFILE=safe
```

Or directly:
```bash
PYTHONPATH=. python scripts/run.py --challenge backblaze-genblaze --profile safe --eval
```

## Key Differentiators
- Media objects (images/video) stored in Backblaze B2
- AI metadata layer: auto-captions, tags, summaries via LLM
- Cost story: B2 free egress + cheap inference = near-zero cost

## References
- Shared ingestion: `core/ingestion/pipeline.py`
- Shared serving: `core/serving/model_server.py`
- Shared eval: `core/evaluation/evaluator.py`
- Challenge config: `challenges/backblaze-genblaze/config.safe.env`
- B2 credentials: set `B2_*` vars in `.env`
