# Architecture Diagram

## Export Instructions

1. Edit `architecture-diagram.excalidraw` (or `.drawio`) in your preferred tool.
2. Export as PNG (1920×1080, white background) → `architecture-diagram.png`
3. Export as SVG (vector) → `architecture-diagram.svg`
4. Commit both exports before submission.

---

## Diagram Elements (reference)

```
┌─────────────────────────────────────────────────┐
│                  Challenge Overlay               │
│  challenges/arm-create/ | backblaze | qwen-cloud │
│  config.safe.env  /  config.aggressive.env       │
└────────────────────┬────────────────────────────┘
                     │ overrides
┌────────────────────▼────────────────────────────┐
│                   Core Pipeline                  │
│                                                  │
│  [Ingestion]──►[Model Serving]──►[Evaluation]   │
│  core/ingestion  core/serving   core/evaluation  │
│                                                  │
│              [Demo UI Shell]                     │
│              core/ui/app.py                      │
└─────────────────────────────────────────────────┘
         │                           │
    config/safe.env        benchmarks/*.json
    config/aggressive.env  benchmarks/*.csv
                           benchmarks/report.md
```

---

## Tool Recommendations
- **Excalidraw** (free, browser-based): https://excalidraw.com
- **draw.io / diagrams.net** (free, offline): https://app.diagrams.net
- **Mermaid** (markdown-native): paste the ASCII above into a Mermaid renderer
