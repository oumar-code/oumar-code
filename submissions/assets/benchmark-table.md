# Benchmark Table Template — Before / After Optimisation

## Instructions
1. Run baseline (stub model): `make benchmark`
2. Configure real model in `.env`
3. Run optimised: `make benchmark CHALLENGE=[name]`
4. Fill in the table below.

---

## Before / After Comparison

| Challenge | Profile | Metric | Before (baseline) | After (optimised) | Delta |
|---|---|---|---|---|---|
| arm-create | safe | quality_score | 1.0 (stub) | | |
| arm-create | safe | avg_latency_ms | 0 (stub) | | |
| arm-create | safe | cost_per_run | $0.00 | | |
| arm-create | safe | reliability | 1.0 | | |
| backblaze-genblaze | safe | quality_score | 1.0 (stub) | | |
| backblaze-genblaze | safe | avg_latency_ms | 0 (stub) | | |
| backblaze-genblaze | safe | cost_per_run | $0.00 | | |
| backblaze-genblaze | safe | reliability | 1.0 | | |
| qwen-cloud | safe | quality_score | 1.0 (stub) | | |
| qwen-cloud | safe | avg_latency_ms | 0 (stub) | | |
| qwen-cloud | safe | cost_per_run | $0.00 | | |
| qwen-cloud | safe | reliability | 1.0 | | |

---

## Machine-Readable Output
All runs auto-save to `benchmarks/` as JSON + CSV.  
Use `benchmarks/report.json` for programmatic access.
