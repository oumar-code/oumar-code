# Kaggriculture — Farming Agent (Scaffold)

This directory contains scaffolding for the Kaggriculture farming-sim hackathon: baseline harness, local validation episode runner, submission packaging, and analytics helpers.

Quick start
1. Create a Python virtualenv and install requirements:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r challenges/kaggriculture/requirements.txt

2. Run a local validation episode (agent vs copy):
   python challenges/kaggriculture/harness/validate.py --agent challenges/kaggriculture/agent/baseline_agent.py

3. Package agent for submission:
   bash challenges/kaggriculture/submission/pack_and_upload.sh --agent challenges/kaggriculture/agent --out submissions/agent_submission.zip

Contents
- agent/ — baseline agent implementation (rule-based, deterministic)
- harness/ — local environment simulator and validation runner (mocks platform validation)
- submission/ — packaging & upload helper (placeholder upload step)
- tests/ — scripts to run local episodes and reproduce logs
- analytics/ — metrics and logging helpers (start here for ladder tracking)

Design notes
- Start with a strong rule-based agent first to reliably pass validation episodes. Later develop RL/hybrid agents.
- Validation harness mimics the platform's "validation episode": it runs the agent against a copy of itself and checks for runtime errors. Use it locally to reproduce failures and collect logs.
- Keep the agent deterministic for validation; enable stochastic options when experimenting for ladder matches.

