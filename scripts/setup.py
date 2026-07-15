#!/usr/bin/env python3
"""
setup.py — environment bootstrap script.
Run once after cloning: python scripts/setup.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: str) -> None:
    print(f"$ {cmd}")
    subprocess.check_call(cmd, shell=True)


def main() -> None:
    # 1. Copy .env.example → .env if not present
    env_example = Path(".env.example")
    env_file = Path(".env")
    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("[setup] Created .env from .env.example — fill in your API keys.")
    else:
        print("[setup] .env already exists — skipping copy.")

    # 2. Install Python dependencies
    req = Path("requirements.txt")
    if req.exists():
        run(f"{sys.executable} -m pip install -r requirements.txt -q")
    else:
        print("[setup] No requirements.txt found — skipping pip install.")

    # 3. Ensure benchmarks directory exists
    Path("benchmarks").mkdir(exist_ok=True)
    print("[setup] benchmarks/ directory ready.")

    print("\n✅  Setup complete.  Run 'make run' or 'python run.py' to start.")


if __name__ == "__main__":
    main()
