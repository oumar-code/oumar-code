#!/usr/bin/env python3
"""
run.py — unified entry-point for any challenge + profile combination.

Usage:
    python run.py --challenge arm-create --profile safe
    python run.py --challenge backblaze-genblaze --profile aggressive
    python run.py --challenge qwen-cloud --profile safe --eval
    python run.py --demo          # interactive CLI demo
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path


def load_challenge_config(challenge: str, profile: str) -> dict:
    """Merge base config → challenge config → profile override."""
    base = _read_env(Path("config") / "safe.env" if profile == "safe" else Path("config") / "aggressive.env")
    challenge_cfg_path = Path("challenges") / challenge / f"config.{profile}.env"
    if challenge_cfg_path.exists():
        base.update(_read_env(challenge_cfg_path))
    return base


def _read_env(path: Path) -> dict:
    result = {}
    if not path.exists():
        return result
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            result[k.strip()] = v.strip()
    return result


def apply_env(env_dict: dict) -> None:
    for k, v in env_dict.items():
        os.environ.setdefault(k, v)


def main() -> None:
    parser = argparse.ArgumentParser(description="Hackathon runner")
    parser.add_argument("--challenge", default="demo", help="Challenge name")
    parser.add_argument("--profile", default="safe", choices=["safe", "aggressive"])
    parser.add_argument("--eval", action="store_true", help="Run evaluation after inference")
    parser.add_argument("--benchmark", action="store_true", help="Alias for --eval")
    parser.add_argument("--demo", action="store_true", help="Launch interactive demo UI")
    args = parser.parse_args()

    env = load_challenge_config(args.challenge, args.profile)
    apply_env(env)
    os.environ["CHALLENGE"] = args.challenge
    os.environ["PROFILE"] = args.profile

    print(f"[run] challenge={args.challenge}  profile={args.profile}")

    if args.demo:
        from core.ui.app import cli_demo
        cli_demo()
        return

    if args.eval or args.benchmark:
        from core.evaluation.evaluator import run_eval, save_results
        result = run_eval(challenge=args.challenge, profile=args.profile)
        json_path, csv_path = save_results(result)
        summary = {k: v for k, v in asdict(result).items() if k != "raw"}
        print(json.dumps(summary, indent=2))
        return

    # Default: run ingestion + serving and print results
    from core.ingestion.pipeline import run_ingestion
    from core.serving.model_server import batch_infer

    records = run_ingestion()
    prompts = [r.get("prompt", str(r)) for r in records]
    responses = batch_infer(prompts)
    for rec, resp in zip(records, responses):
        print(f"  [{rec.get('id', '?')}] {resp['text'][:100]}")


if __name__ == "__main__":
    main()
