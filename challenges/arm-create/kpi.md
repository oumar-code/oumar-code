# Arm Create — KPI Emphasis

## Most Important Metrics (in priority order)

1. **`avg_latency_ms`** — Primary KPI. Judges look for sub-second response on Arm hardware.
2. **`cost_per_run`** — Directly tied to efficiency story; lower = better.
3. **`reliability`** — Must be ≥ 0.98; any demo crash is disqualifying.
4. **`quality_score`** — Secondary; correctness matters but speed wins the room.

## Threshold Targets

| Metric | Minimum Passing | Gold Target |
|---|---|---|
| avg_latency_ms | ≤ 1500 | ≤ 500 |
| cost_per_run | ≤ $0.10 | ≤ $0.02 |
| reliability | ≥ 0.95 | ≥ 0.99 |
| quality_score | ≥ 0.70 | ≥ 0.90 |

## Story Framing
Lead with **efficiency + cost**: "We run the same quality at 3× lower cost on Arm."
