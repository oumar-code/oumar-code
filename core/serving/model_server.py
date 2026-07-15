"""
Model Serving Layer
===================
Thin wrapper around any LLM endpoint.  Reads MODEL_ENDPOINT and MODEL_NAME
from environment (or .env).  Falls back to a stub response so demos never crash.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class ServingConfig:
    endpoint: str = ""          # set via MODEL_ENDPOINT env var
    model: str = "stub"         # set via MODEL_NAME env var
    timeout: float = 30.0
    max_tokens: int = 512
    temperature: float = 0.7


def _resolve_config(cfg: ServingConfig | None) -> ServingConfig:
    cfg = cfg or ServingConfig()
    cfg.endpoint = cfg.endpoint or os.getenv("MODEL_ENDPOINT", "")
    cfg.model = cfg.model if cfg.model != "stub" else os.getenv("MODEL_NAME", "stub")
    return cfg


def _stub_response(prompt: str) -> dict[str, Any]:
    """Safe fallback when no real endpoint is configured."""
    return {
        "text": f"[STUB] Echo: {prompt[:80]}",
        "model": "stub",
        "latency_ms": 0,
        "tokens_used": 0,
    }


def _call_endpoint(prompt: str, cfg: ServingConfig) -> dict[str, Any]:
    """Call a real OpenAI-compatible endpoint."""
    try:
        import httpx  # optional dep — only needed for live runs

        t0 = time.perf_counter()
        resp = httpx.post(
            cfg.endpoint,
            json={
                "model": cfg.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": cfg.max_tokens,
                "temperature": cfg.temperature,
            },
            timeout=cfg.timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        latency_ms = int((time.perf_counter() - t0) * 1000)
        text = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", 0)
        return {"text": text, "model": cfg.model, "latency_ms": latency_ms, "tokens_used": tokens}
    except Exception as exc:  # noqa: BLE001
        return {"text": f"[ERROR] {exc}", "model": cfg.model, "latency_ms": -1, "tokens_used": 0}


def infer(prompt: str, cfg: ServingConfig | None = None) -> dict[str, Any]:
    """Run inference — stubs gracefully when no endpoint is configured."""
    cfg = _resolve_config(cfg)
    if not cfg.endpoint:
        return _stub_response(prompt)
    return _call_endpoint(prompt, cfg)


def batch_infer(prompts: list[str], cfg: ServingConfig | None = None) -> list[dict[str, Any]]:
    cfg = _resolve_config(cfg)
    return [infer(p, cfg) for p in prompts]


if __name__ == "__main__":
    result = infer("What is 2 + 2?")
    print(result)
