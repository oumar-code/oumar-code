# Qwen Cloud — Submission Checklist

## Pre-Submission (T-24h)
- [ ] Multilingual test data in `data/inputs.jsonl` (≥ 3 languages)
- [ ] `make eval CHALLENGE=qwen-cloud PROFILE=safe` passes
- [ ] quality_score ≥ 0.85 across all tested languages
- [ ] Cloud deployment notes documented

## Benchmark Artifacts
- [ ] `benchmarks/qwen-cloud_safe_*.json` committed
- [ ] `benchmarks/qwen-cloud_aggressive_*.json` committed
- [ ] Multi-language breakdown in benchmark notes

## Submission Package
- [ ] `submissions/assets/technical-writeup.md` Qwen section complete
- [ ] `submissions/assets/impact-narrative.md` multilingual story
- [ ] Architecture diagram shows cloud-native scaling path

## Final (T-1h)
- [ ] Re-run `make benchmark CHALLENGE=qwen-cloud`
- [ ] Multi-language demo rehearsed (show 2+ languages)
- [ ] Repo pushed, PR opened
