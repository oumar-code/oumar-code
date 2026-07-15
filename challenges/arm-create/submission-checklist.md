# Arm Create — Submission Checklist

## Pre-Submission (T-24h)
- [ ] `make eval CHALLENGE=arm-create PROFILE=safe` passes with no errors
- [ ] `benchmarks/arm-create_safe_*.json` committed and latency ≤ 800 ms
- [ ] Demo runs end-to-end on Arm instance (or emulated Arm)
- [ ] Architecture diagram updated with Arm-specific notes

## Benchmark Artifacts
- [ ] `benchmarks/arm-create_safe_*.json`
- [ ] `benchmarks/arm-create_aggressive_*.json`
- [ ] `benchmarks/baseline.md` table updated with real values

## Submission Package
- [ ] `submissions/assets/technical-writeup.md` filled (Arm section)
- [ ] `submissions/assets/benchmark-table.md` populated
- [ ] 2-minute demo script rehearsed
- [ ] Backup demo script ready

## Final (T-1h)
- [ ] Re-run `make benchmark` — confirm numbers match narrative
- [ ] Architecture diagram exported as PNG
- [ ] Repo pushed, PR opened
