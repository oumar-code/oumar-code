# Backblaze Genblaze — Submission Checklist

## Pre-Submission (T-24h)
- [ ] B2 credentials set in `.env` (never committed)
- [ ] `make eval CHALLENGE=backblaze-genblaze PROFILE=safe` passes
- [ ] B2 bucket created and accessible
- [ ] End-to-end flow demonstrated: ingest → AI tag → B2 upload → retrieve

## Benchmark Artifacts
- [ ] `benchmarks/backblaze-genblaze_safe_*.json` committed
- [ ] `benchmarks/backblaze-genblaze_aggressive_*.json` committed
- [ ] cost_per_run clearly shows B2 free-egress advantage

## Submission Package
- [ ] `submissions/assets/technical-writeup.md` Backblaze section complete
- [ ] `submissions/assets/impact-narrative.md` media workflow story
- [ ] Architecture diagram shows B2 integration

## Final (T-1h)
- [ ] Re-run `make benchmark CHALLENGE=backblaze-genblaze`
- [ ] B2 bucket URL / screenshot in assets
- [ ] Repo pushed, PR opened
