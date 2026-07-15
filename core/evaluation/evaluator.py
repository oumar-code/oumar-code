"""
Evaluation & Benchmarking Engine
==================================
Runs inference over a dataset, records metrics, and writes results to
benchmarks/<run_id>.json and benchmarks/<run_id>.csv.
"""
from __future__ import annotations

import csv
import json
import os
import statistics
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from core.ingestion.pipeline import IngestionConfig, run_ingestion
from core.serving.model_server import ServingConfig, batch_infer


@dataclass
class EvalResult:
    run_id: str
    challenge: str
    profile: str                 # safe | aggressive
    model: str
    timestamp: str
    total_samples: int
    avg_latency_ms: float
    p95_latency_ms: float
    avg_tokens: float
    error_rate: float
    cost_per_run: float          # estimated USD; 0.0 if unknown
    quality_score: float         # 0-1; filled by downstream judge / heuristic
    reliability: float           # 1 - error_rate
    notes: str = ""
    raw: list[dict[str, Any]] = field(default_factory=list)


def _estimate_cost(total_tokens: int, model: str) -> float:
    """Very rough cost estimate — override per-challenge if needed."""
    rate = float(os.getenv("COST_PER_1K_TOKENS", "0.002"))
    return round(total_tokens / 1000 * rate, 6)


def run_eval(
    challenge: str = "demo",
    profile: str = "safe",
    ingestion_cfg: IngestionConfig | None = None,
    serving_cfg: ServingConfig | None = None,
    quality_fn: Any = None,
) -> EvalResult:
    """
    End-to-end evaluation run.
    *quality_fn(record, response) -> float* is optional; defaults to 1.0 stub.
    """
    run_id = str(uuid.uuid4())[:8]
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    records = run_ingestion(ingestion_cfg)
    prompts = [r.get("prompt", str(r)) for r in records]

    responses = batch_infer(prompts, serving_cfg)

    latencies = [r["latency_ms"] for r in responses]
    tokens = [r["tokens_used"] for r in responses]
    errors = [r for r in responses if r["latency_ms"] < 0]
    quality_scores = []
    for rec, resp in zip(records, responses):
        if quality_fn:
            quality_scores.append(float(quality_fn(rec, resp)))
        else:
            quality_scores.append(1.0 if resp["latency_ms"] >= 0 else 0.0)

    avg_lat = statistics.mean(latencies) if latencies else 0
    if len(latencies) > 1:
        p95_lat = sorted(latencies)[min(int(len(latencies) * 0.95), len(latencies) - 1)]
    elif latencies:
        p95_lat = latencies[0]
    else:
        p95_lat = 0
    avg_tok = statistics.mean(tokens) if tokens else 0
    total_tok = sum(tokens)
    error_rate = len(errors) / max(len(responses), 1)
    quality = statistics.mean(quality_scores) if quality_scores else 0

    model_name = responses[0]["model"] if responses else "unknown"

    result = EvalResult(
        run_id=run_id,
        challenge=challenge,
        profile=profile,
        model=model_name,
        timestamp=timestamp,
        total_samples=len(records),
        avg_latency_ms=round(avg_lat, 2),
        p95_latency_ms=round(p95_lat, 2),
        avg_tokens=round(avg_tok, 2),
        error_rate=round(error_rate, 4),
        cost_per_run=_estimate_cost(total_tok, model_name),
        quality_score=round(quality, 4),
        reliability=round(1 - error_rate, 4),
        raw=responses,
    )
    return result


def save_results(result: EvalResult, out_dir: str = "benchmarks") -> tuple[Path, Path]:
    """Write JSON + CSV artifacts."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    base = f"{result.challenge}_{result.profile}_{result.run_id}"

    json_path = Path(out_dir) / f"{base}.json"
    csv_path = Path(out_dir) / f"{base}.csv"

    # JSON — full detail
    payload = asdict(result)
    payload.pop("raw")           # keep artifacts lean; raw is in-memory only
    json_path.write_text(json.dumps(payload, indent=2))

    # CSV — summary row
    fields = [
        "run_id", "challenge", "profile", "model", "timestamp",
        "total_samples", "avg_latency_ms", "p95_latency_ms", "avg_tokens",
        "error_rate", "cost_per_run", "quality_score", "reliability",
    ]
    row = {k: getattr(result, k) for k in fields}
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"[eval] JSON → {json_path}")
    print(f"[eval] CSV  → {csv_path}")
    return json_path, csv_path


if __name__ == "__main__":
    result = run_eval()
    save_results(result)
    print(json.dumps(
        {k: v for k, v in asdict(result).items() if k != "raw"},
        indent=2,
    ))
