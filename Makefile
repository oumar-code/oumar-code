.PHONY: setup run eval benchmark demo clean help

PYTHON := python3
CHALLENGE ?= demo
PROFILE   ?= safe

## ── Bootstrap ──────────────────────────────────────────────────────────────
setup:           ## Install deps and create .env
	$(PYTHON) scripts/setup.py

## ── Run ─────────────────────────────────────────────────────────────────────
run:             ## Run ingestion + inference (default challenge/profile)
	$(PYTHON) -m scripts.run --challenge $(CHALLENGE) --profile $(PROFILE)

run-safe:        ## Run with stable defaults
	$(PYTHON) -m scripts.run --challenge $(CHALLENGE) --profile safe

run-aggressive:  ## Run with experimental settings
	$(PYTHON) -m scripts.run --challenge $(CHALLENGE) --profile aggressive

demo:            ## Launch interactive CLI demo
	$(PYTHON) -m scripts.run --demo

demo-ui:         ## Launch Gradio web demo (requires: pip install gradio)
	$(PYTHON) core/ui/app.py --gradio

## ── Eval / Benchmark ─────────────────────────────────────────────────────
eval:            ## Evaluate current CHALLENGE + PROFILE
	$(PYTHON) -m scripts.run --challenge $(CHALLENGE) --profile $(PROFILE) --eval

benchmark:       ## Full benchmark sweep across all challenges × profiles
	$(PYTHON) scripts/benchmark.py

## ── Challenge shortcuts ──────────────────────────────────────────────────
arm-safe:
	$(MAKE) run CHALLENGE=arm-create PROFILE=safe

arm-aggressive:
	$(MAKE) run CHALLENGE=arm-create PROFILE=aggressive

backblaze-safe:
	$(MAKE) run CHALLENGE=backblaze-genblaze PROFILE=safe

backblaze-aggressive:
	$(MAKE) run CHALLENGE=backblaze-genblaze PROFILE=aggressive

qwen-safe:
	$(MAKE) run CHALLENGE=qwen-cloud PROFILE=safe

qwen-aggressive:
	$(MAKE) run CHALLENGE=qwen-cloud PROFILE=aggressive

## ── OpenAI Build Week — Fashion App ─────────────────────────────────────
fashion-safe:            ## Run Fashion Tutor Agent (safe profile)
	$(MAKE) run CHALLENGE=openai-fashion PROFILE=safe

fashion-aggressive:      ## Run Fashion app (aggressive / higher creativity)
	$(MAKE) run CHALLENGE=openai-fashion PROFILE=aggressive

fashion-eval:            ## Evaluate Fashion challenge (safe profile)
	$(MAKE) eval CHALLENGE=openai-fashion PROFILE=safe

fashion-demo-python:     ## Run Python fashion module demos
	$(PYTHON) -m fashion.agent && $(PYTHON) -m fashion.pattern_math && $(PYTHON) -m fashion.copilot

fashion-demo-ui:         ## Launch Next.js fashion frontend (requires: cd frontend && npm install)
	cd frontend && npm run dev

fashion-checklist:       ## View submission checklist
	cat challenges/openai-fashion/submission-checklist.md

## ── Housekeeping ────────────────────────────────────────────────────────
clean:           ## Remove generated benchmark artifacts
	rm -rf benchmarks/*.json benchmarks/*.csv benchmarks/report.*

help:            ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
