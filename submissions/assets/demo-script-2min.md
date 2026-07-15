# 2-Minute Live Demo Script

> **Total time: 120 seconds**  
> Rehearse until you can hit every beat without looking at notes.

---

## T+0:00 — Hook (15 s)
> "Imagine deploying a production-grade AI pipeline for any hackathon challenge in under five commands. That's what we built."

**Action:** show terminal, run:
```bash
make setup
make run CHALLENGE=[CHALLENGE] PROFILE=safe
```

---

## T+0:15 — The Problem (20 s)
> "[1 sentence on the challenge pain point — fill in per challenge]"  
> "Today, [status quo].  We changed that."

---

## T+0:35 — The Solution (30 s)
> "We built a shared backbone — ingestion, model serving, evaluation — that adapts to any challenge with a single config swap."

**Action:** show `config/safe.env` vs `challenges/[CHALLENGE]/config.safe.env` side by side.

---

## T+1:05 — Live Demo (30 s)
```bash
make eval CHALLENGE=[CHALLENGE] PROFILE=safe
```
**Point at output:**  
- quality_score: [X]  
- avg_latency_ms: [Y]  
- cost_per_run: $[Z]

> "Best-in-class quality, sub-second latency, cents per run."

---

## T+1:35 — Impact & Close (25 s)
> "[Fill impact narrative — who benefits, why now, why this team]"  
> "The code is open, the results speak for themselves.  Thank you."

---

## Backup lines (if live demo fails)
- "Let me show you the pre-recorded run…" → open `benchmarks/baseline.md`
- "The numbers here are from our last clean run…" → point at committed JSON
