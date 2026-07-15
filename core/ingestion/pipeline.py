"""
Ingestion & Orchestration Pipeline
===================================
Shared entry point for loading data / prompt batches and routing them
to the model-serving layer.  Override `load_inputs` for your challenge.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator


@dataclass
class IngestionConfig:
    source: str = "data/inputs.jsonl"          # local file or URL
    batch_size: int = 8
    max_samples: int | None = None             # None = all
    extra: dict[str, Any] = field(default_factory=dict)


def load_inputs(cfg: IngestionConfig) -> Iterator[list[dict]]:
    """Yield batches of records from *cfg.source* (JSONL or JSON array)."""
    path = Path(cfg.source)
    records: list[dict] = []

    if path.exists():
        with path.open() as fh:
            for line in fh:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    else:
        # Fallback: single synthetic sample so the pipeline can always run
        records = [{"id": "demo-0", "prompt": "Hello, world!"}]

    if cfg.max_samples is not None:
        records = records[: cfg.max_samples]

    for i in range(0, max(1, len(records)), cfg.batch_size):
        yield records[i : i + cfg.batch_size]


def run_ingestion(cfg: IngestionConfig | None = None) -> list[dict]:
    """Collect all records and return a flat list."""
    cfg = cfg or IngestionConfig()
    all_records: list[dict] = []
    for batch in load_inputs(cfg):
        all_records.extend(batch)
    return all_records


if __name__ == "__main__":
    records = run_ingestion()
    print(f"Ingested {len(records)} record(s).")
    print(records[:2])
