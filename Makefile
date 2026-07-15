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

## ── Housekeeping ────────────────────────────────────────────────────────
clean:           ## Remove generated benchmark artifacts
	rm -rf benchmarks/*.json benchmarks/*.csv benchmarks/report.*

help:            ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
