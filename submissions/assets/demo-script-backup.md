# Full Backup Demo Script

> Use this if the live environment fails.  All outputs are pre-recorded.

## Setup (run before the room fills)
```bash
# Pre-generate all artifacts
make benchmark
# Verify outputs exist
ls benchmarks/*.json benchmarks/*.md
```

## Script

### Slide 1 — Problem (30 s)
> "[Challenge-specific pain point]"

### Slide 2 — Architecture (45 s)
Walk through `submissions/assets/architecture-diagram.[png|svg]`:
- Left: Data Ingestion (`core/ingestion/`)
- Centre: Model Serving (`core/serving/`) — safe vs aggressive profile
- Right: Evaluation Engine (`core/evaluation/`)
- Bottom: Challenge overlays (`challenges/[name]/`)

### Slide 3 — Benchmark Results (45 s)
Show `benchmarks/baseline.md` table.  
Narrate key numbers:  
- quality_score vs baseline  
- latency improvement  
- cost comparison

### Slide 4 — Impact (30 s)
> "[Impact narrative from submissions/assets/impact-narrative.md]"

### Slide 5 — Next Steps (30 s)
> "With X more days, we would add Y.  The backbone is extensible by design."

## Fallback for laptop failure
- PDF export of slides in `submissions/assets/backup-slides.pdf`
- Printed benchmark table as physical backup
