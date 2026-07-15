# Final-Day Submission Runbook

> Follow this exactly. Do not skip steps. Times are guidelines — adjust for your challenge window.

---

## T-24h: Freeze & Verify

| Time | Action | Owner |
|---|---|---|
| T-24h | `git pull origin main` — sync latest | All |
| T-24h | `make benchmark` — full sweep, no errors | Dev |
| T-24h | Fill `submissions/assets/benchmark-table.md` with real numbers | Dev |
| T-23h | Export architecture diagram PNG | Design |
| T-22h | Complete `submissions/assets/technical-writeup.md` | All |
| T-20h | Rehearse 2-min demo script (3× run-through) | All |

---

## T-4h: Package

```bash
# 1. Final benchmark run
make benchmark

# 2. Verify artifacts
ls benchmarks/

# 3. Commit everything
git add benchmarks/ submissions/ challenges/
git commit -m "chore: final benchmark artifacts + submission docs"
git push
```

---

## T-2h: Submission Checklist

- [ ] All benchmark JSON/CSV in `benchmarks/`
- [ ] `submissions/assets/technical-writeup.md` complete
- [ ] `submissions/assets/benchmark-table.md` complete  
- [ ] `submissions/assets/architecture-diagram.png` exported
- [ ] `submissions/assets/impact-narrative.md` complete
- [ ] Demo rehearsed and working
- [ ] Backup demo script ready
- [ ] Submission form link open and pre-filled
- [ ] Per-challenge submission checklist done (see `challenges/[name]/submission-checklist.md`)

---

## T-0: Submit

1. Open submission form
2. Paste repo URL
3. Attach `submissions/assets/technical-writeup.md`
4. Attach `benchmarks/report.md`
5. Attach `submissions/assets/architecture-diagram.png`
6. Submit ✅

---

## If Things Break

| Scenario | Response |
|---|---|
| Live demo fails | Switch to backup demo script immediately |
| Benchmark numbers missing | Use `benchmarks/baseline.md` committed values |
| API key expired | Demo runs in stub mode — show architecture instead |
| Repo access down | Demo from local `benchmarks/report.md` printout |
