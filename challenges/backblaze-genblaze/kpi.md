# Backblaze Genblaze — KPI Emphasis

## Most Important Metrics (in priority order)

1. **B2 pipeline reliability** — Demo must show successful upload + download from B2.
2. **`quality_score`** — AI-generated metadata must be accurate and useful.
3. **`cost_per_run`** — Backblaze B2 free egress + cheap LLM = zero-cost story.
4. **`avg_latency_ms`** — End-to-end media workflow; 3s is acceptable.

## Threshold Targets

| Metric | Minimum Passing | Gold Target |
|---|---|---|
| reliability | ≥ 0.95 | ≥ 0.99 |
| quality_score | ≥ 0.75 | ≥ 0.90 |
| cost_per_run | ≤ $0.10 | ≤ $0.01 |
| avg_latency_ms | ≤ 5000 | ≤ 2000 |

## Story Framing
Lead with **B2 cost advantage**: "Zero egress fees + AI metadata at cents per thousand assets."
