"""
Demo UI Shell
=============
Minimal Gradio (or plain-text CLI) demo that works with or without a browser.
Install gradio only if you want the web UI; the CLI fallback always works.
"""
from __future__ import annotations

import os
import sys

from core.serving.model_server import ServingConfig, infer


def cli_demo() -> None:
    print("=== Hackathon Demo (CLI mode) ===")
    print("Type your prompt and press Enter. Ctrl+C to quit.\n")
    cfg = ServingConfig()
    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if not prompt:
            continue
        result = infer(prompt, cfg)
        print(f"Model ({result['model']}): {result['text']}")
        print(f"  latency={result['latency_ms']}ms  tokens={result['tokens_used']}\n")


def gradio_demo() -> None:
    import gradio as gr  # type: ignore

    cfg = ServingConfig()

    def respond(prompt: str) -> str:
        result = infer(prompt, cfg)
        meta = f"\n\n---\n*model: {result['model']} | latency: {result['latency_ms']}ms*"
        return result["text"] + meta

    iface = gr.Interface(
        fn=respond,
        inputs=gr.Textbox(label="Prompt", lines=4),
        outputs=gr.Markdown(label="Response"),
        title="Hackathon Demo",
        description=f"Profile: {os.getenv('PROFILE', 'safe')} | Challenge: {os.getenv('CHALLENGE', 'demo')}",
    )
    iface.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("UI_PORT", "7860")),
        share=False,
    )


if __name__ == "__main__":
    use_gradio = "--gradio" in sys.argv
    if use_gradio:
        try:
            gradio_demo()
        except ImportError:
            print("[warn] gradio not installed — falling back to CLI demo.")
            cli_demo()
    else:
        cli_demo()
