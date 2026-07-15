# Technical Write-Up Template

> Fill in each section before submission.  Keep total length under 1000 words.

---

## Executive Summary
[2–3 sentences: what you built, why it matters, one headline metric.]

---

## Problem Statement
[What specific pain point does this address?  Who experiences it?]

---

## Technical Approach

### Architecture Overview
[Reference architecture-diagram.png]

The system is composed of four shared modules:
- **Ingestion** (`core/ingestion/`): loads prompt batches from any source
- **Serving** (`core/serving/`): OpenAI-compatible endpoint wrapper with stub fallback
- **Evaluation** (`core/evaluation/`): metrics collection, JSON + CSV output
- **UI** (`core/ui/`): CLI and optional Gradio web interface

### Challenge-Specific Layer
[Describe what `challenges/[name]/` adds on top of the core.]

---

## Results

| Metric | Baseline (stub) | Our Result | Improvement |
|---|---|---|---|
| quality_score | 1.0 (stub) | [X] | [+Y%] |
| avg_latency_ms | 0 (stub) | [X] | — |
| cost_per_run | $0.00 | $[X] | — |
| reliability | 1.0 | [X] | — |

---

## Arm Create Specifics
[Efficiency gains, quantisation approach, Arm instance type used]

## Backblaze Genblaze Specifics
[B2 integration details, media workflow description, cost comparison]

## Qwen Cloud Specifics
[Languages tested, multilingual quality scores, cloud scaling approach]

---

## Limitations & Future Work
- [ ] Real model integration (currently stub without API key)
- [ ] [Challenge-specific limitation]
- [ ] [What you'd add with more time]

---

## Team
[Names, roles, GitHub handles]
