"""
Tailor Co-pilot
===============
AI agent that helps small-scale tailors and fashion entrepreneurs manage
client orders, generate tech packs, estimate fabric, and quote prices.

The co-pilot uses GPT-5.6 for logic and Codex for structured output
(JSON tech packs, price formulas, markdown order summaries).

Usage
-----
    from fashion.copilot import TailorCopilot

    copilot = TailorCopilot()

    # From a description (or inspo photo analysis)
    result = copilot.generate_tech_pack(
        description="Corporate ankara blazer, size 14, navy/gold print, 3/4 sleeves",
    )
    print(result["tech_pack"])
    print(result["price_quote"])
    print(result["fabric_estimate"])
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Pricing config (adjustable via env or at runtime)
# ---------------------------------------------------------------------------

DEFAULT_PRICING = {
    "labour_rate_per_hour_ngn": 1500,   # ₦1,500/hr (Lagos standard, 2024)
    "material_markup_pct": 20,          # 20% markup on fabric cost
    "overhead_pct": 15,                 # 15% overhead
    "profit_margin_pct": 25,            # 25% profit margin
    "complexity_multipliers": {
        "simple": 1.0,       # e.g. straight skirt
        "moderate": 1.5,     # e.g. dress with zipper and darts
        "complex": 2.5,      # e.g. tailored jacket
        "couture": 4.0,      # e.g. heavily embellished gown
    },
    "fabric_prices_ngn_per_yard": {
        "ankara": 1800,
        "lace": 4500,
        "kente": 8000,
        "aso-oke": 6500,
        "chiffon": 2200,
        "cotton": 1500,
        "silk": 5500,
        "velvet": 3800,
        "denim": 2000,
        "generic": 2000,
    },
}


@dataclass
class TailorCopilot:
    """
    AI-powered co-pilot for tailors and fashion entrepreneurs.

    Falls back to rich stubs so demos work without an API key.
    """
    model: str = field(default_factory=lambda: os.getenv("MODEL_NAME", "gpt-5.6-luna"))
    api_key: str = field(default_factory=lambda: os.getenv("MODEL_API_KEY", ""))
    endpoint: str = field(default_factory=lambda: os.getenv(
        "MODEL_ENDPOINT", "https://api.openai.com/v1/chat/completions"
    ))
    pricing: dict = field(default_factory=lambda: dict(DEFAULT_PRICING))

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def generate_tech_pack(
        self,
        description: str,
        image_analysis: dict | None = None,
    ) -> dict[str, Any]:
        """
        Generate a professional tech pack from a garment description.

        Parameters
        ----------
        description    : free-text description of the garment
        image_analysis : optional output from FashionTutorAgent.analyze_image()

        Returns
        -------
        dict with:
          tech_pack     : structured garment specification (dict)
          price_quote   : pricing breakdown (dict)
          fabric_estimate: fabric yardage + cost estimate (dict)
          summary_md    : markdown summary ready to share with client
        """
        context = description
        if image_analysis:
            context += f"\n\nImage analysis:\n{image_analysis.get('text', '')}"

        if not self.api_key:
            return self._stub_tech_pack(description)

        prompt = _build_tech_pack_prompt(context)
        raw = self._call_llm(prompt)

        if raw.get("latency_ms", -1) < 0:
            return self._stub_tech_pack(description)

        parsed = _parse_tech_pack_response(raw["text"])
        fabric_est = self.estimate_fabric_cost(parsed.get("fabric_type", "generic"),
                                               parsed.get("fabric_yards", 4.0))
        price = self.calculate_price(
            fabric_cost_ngn=fabric_est["fabric_cost_ngn"],
            complexity=parsed.get("complexity", "moderate"),
            hours=parsed.get("estimated_hours", 6.0),
        )
        summary = _format_summary_md(parsed, price, fabric_est)
        return {
            "tech_pack": parsed,
            "price_quote": price,
            "fabric_estimate": fabric_est,
            "summary_md": summary,
            "latency_ms": raw["latency_ms"],
        }

    def estimate_fabric_cost(
        self,
        fabric_type: str = "generic",
        yards: float = 4.0,
        currency: str = "NGN",
    ) -> dict[str, Any]:
        """
        Estimate fabric cost for a garment.

        Parameters
        ----------
        fabric_type : fabric name (ankara, lace, kente, etc.)
        yards       : fabric yardage required
        currency    : output currency label
        """
        prices = self.pricing["fabric_prices_ngn_per_yard"]
        price_per_yard = prices.get(fabric_type.lower(), prices["generic"])
        total_ngn = price_per_yard * yards
        markup = total_ngn * (self.pricing["material_markup_pct"] / 100)

        return {
            "fabric_type": fabric_type,
            "yards": yards,
            "price_per_yard_ngn": price_per_yard,
            "fabric_cost_ngn": round(total_ngn),
            "cost_with_markup_ngn": round(total_ngn + markup),
            "currency": currency,
            "note": "Add 10% for print matching on patterned fabrics",
        }

    def calculate_price(
        self,
        fabric_cost_ngn: float,
        complexity: str = "moderate",
        hours: float = 6.0,
    ) -> dict[str, Any]:
        """
        Calculate a full price quote for a garment.

        Parameters
        ----------
        fabric_cost_ngn : total fabric cost in Naira
        complexity      : simple | moderate | complex | couture
        hours           : estimated labour hours
        """
        rate = self.pricing["labour_rate_per_hour_ngn"]
        multiplier = self.pricing["complexity_multipliers"].get(complexity, 1.5)
        overhead_pct = self.pricing["overhead_pct"] / 100
        profit_pct = self.pricing["profit_margin_pct"] / 100

        labour = rate * hours * multiplier
        overhead = (fabric_cost_ngn + labour) * overhead_pct
        subtotal = fabric_cost_ngn + labour + overhead
        profit = subtotal * profit_pct
        total = subtotal + profit

        return {
            "complexity": complexity,
            "labour_hours": hours,
            "fabric_cost_ngn": round(fabric_cost_ngn),
            "labour_cost_ngn": round(labour),
            "overhead_ngn": round(overhead),
            "profit_ngn": round(profit),
            "total_ngn": round(total),
            "total_usd_approx": round(total / 1600, 2),  # ~₦1600/$1 2024
            "breakdown_pct": {
                "fabric": round(fabric_cost_ngn / total * 100, 1),
                "labour": round(labour / total * 100, 1),
                "overhead": round(overhead / total * 100, 1),
                "profit": round(profit / total * 100, 1),
            },
        }

    def generate_order_summary(self, order: dict) -> str:
        """
        Generate a client-ready order confirmation message (WhatsApp/SMS friendly).

        Parameters
        ----------
        order : dict with keys: client_name, garment, size, fabric, deadline, price_quote
        """
        name = order.get("client_name", "Customer")
        garment = order.get("garment", "garment")
        size = order.get("size", "")
        fabric = order.get("fabric", "")
        deadline = order.get("deadline", "TBD")
        price = order.get("price_quote", {})
        total = price.get("total_ngn", 0)

        return f"""\
✂️ *Order Confirmation*
━━━━━━━━━━━━━━━━━━━━
👤 Client: {name}
👗 Garment: {garment}{f' (Size {size})' if size else ''}
🧵 Fabric: {fabric}
📅 Ready by: {deadline}
💰 Total: ₦{total:,}
━━━━━━━━━━━━━━━━━━━━
Payment: 50% deposit (₦{total // 2:,}) to confirm.
Balance on delivery.

Thank you for choosing us! 🙏
*Powered by Aku Fashion Co-pilot*
"""

    # -----------------------------------------------------------------------
    # Internal
    # -----------------------------------------------------------------------

    def _call_llm(self, prompt: str) -> dict[str, Any]:
        try:
            import httpx
        except ImportError:
            return {"text": "[stub]", "latency_ms": 0}

        t0 = time.perf_counter()
        try:
            resp = httpx.post(
                self.endpoint,
                headers={
                    "Authorization": f"******",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": _COPILOT_SYSTEM},
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": 1024,
                    "temperature": 0.3,
                },
                timeout=60.0,
            )
            resp.raise_for_status()
            data = resp.json()
            latency_ms = int((time.perf_counter() - t0) * 1000)
            return {"text": data["choices"][0]["message"]["content"], "latency_ms": latency_ms}
        except Exception as exc:  # noqa: BLE001
            return {"text": f"[ERROR] {exc}", "latency_ms": -1}

    def _stub_tech_pack(self, description: str) -> dict[str, Any]:
        """Rich demo stub for tech pack generation."""
        tech_pack = {
            "garment_name": "Corporate Ankara Blazer",
            "description": description,
            "category": "Outerwear",
            "silhouette": "Fitted / Structured",
            "fabric_type": "ankara",
            "fabric_yards": 4.5,
            "colour": "Navy + Gold Print",
            "lining": "Polyester lining, full body",
            "closure": "3 × functional buttons, front",
            "sleeves": "3/4 length, 2-button cuff",
            "collar": "Notch lapel",
            "pockets": "2 × welt pockets at chest, 2 × flap pockets at hip",
            "complexity": "complex",
            "estimated_hours": 12.0,
            "size_range": "XS–3XL",
            "seam_allowance_cm": 1.5,
            "special_notes": [
                "Match print at centre front, shoulder seams, and pocket flaps",
                "Pad stitch lapels by hand for structure",
                "Press all seams flat with tailor's ham",
            ],
            "construction_order": [
                "1. Interface all structural pieces (fronts, collar, cuffs)",
                "2. Sew and press all darts",
                "3. Construct welt pockets before joining side seams",
                "4. Join shoulder seams, press open",
                "5. Attach and set sleeves",
                "6. Construct and attach collar/lapels",
                "7. Join side seams",
                "8. Construct lining separately, attach at hem",
                "9. Hand sew buttons and bound buttonholes",
                "10. Final pressing with pressing cloth",
            ],
        }

        fabric_est = self.estimate_fabric_cost("ankara", 4.5)
        price = self.calculate_price(
            fabric_cost_ngn=fabric_est["fabric_cost_ngn"],
            complexity="complex",
            hours=12.0,
        )
        summary = _format_summary_md(tech_pack, price, fabric_est)

        return {
            "tech_pack": tech_pack,
            "price_quote": price,
            "fabric_estimate": fabric_est,
            "summary_md": summary,
            "latency_ms": 0,
        }


# ---------------------------------------------------------------------------
# Prompts and parsers
# ---------------------------------------------------------------------------

_COPILOT_SYSTEM = """\
You are an expert fashion tech pack writer and tailoring business consultant.
Output structured, professional garment specifications.
Always output valid JSON when requested. Be precise about measurements.
"""


def _build_tech_pack_prompt(description: str) -> str:
    return f"""\
Create a complete tech pack for the following garment:

{description}

Output a JSON object with these fields:
- garment_name, description, category, silhouette
- fabric_type (ankara/lace/cotton/etc.), fabric_yards (float)
- colour, lining, closure, sleeves, collar, pockets
- complexity (simple/moderate/complex/couture)
- estimated_hours (float — total labour hours)
- special_notes (list of strings)
- construction_order (numbered list of steps)

Be specific and professional. All measurements in centimetres.
"""


def _parse_tech_pack_response(text: str) -> dict:
    """Extract JSON from LLM response."""
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        return {"description": text, "complexity": "moderate",
                "fabric_type": "generic", "fabric_yards": 4.0, "estimated_hours": 6.0}


def _format_summary_md(tech_pack: dict, price: dict, fabric: dict) -> str:
    name = tech_pack.get("garment_name", "Garment")
    total = price.get("total_ngn", 0)
    fabric_yards = fabric.get("yards", 0)
    fabric_type = fabric.get("fabric_type", "fabric")
    hours = price.get("labour_hours", 0)

    notes = tech_pack.get("special_notes", [])
    notes_md = "\n".join(f"- {n}" for n in notes) if notes else "- None"

    steps = tech_pack.get("construction_order", [])
    steps_md = "\n".join(str(s) for s in steps) if steps else "See tech pack"

    return f"""\
# Tech Pack: {name}

## Overview
| Field | Value |
|---|---|
| Category | {tech_pack.get('category', '—')} |
| Silhouette | {tech_pack.get('silhouette', '—')} |
| Fabric | {fabric_type.title()} ({fabric_yards} yards) |
| Complexity | {price.get('complexity', '—').title()} |
| Labour Hours | {hours}h |

## Price Quote
| Item | Amount (₦) |
|---|---|
| Fabric | {price.get('fabric_cost_ngn', 0):,} |
| Labour | {price.get('labour_cost_ngn', 0):,} |
| Overhead | {price.get('overhead_ngn', 0):,} |
| Profit | {price.get('profit_ngn', 0):,} |
| **Total** | **{total:,}** |

> *Approx. ${price.get('total_usd_approx', 0)} USD*

## Special Notes
{notes_md}

## Construction Order
{steps_md}

---
*Generated by Aku Fashion Co-pilot — powered by GPT-5.6*
"""


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    copilot = TailorCopilot()

    print("=== Tailor Co-pilot Demo ===\n")

    result = copilot.generate_tech_pack(
        "Corporate ankara blazer, size 14, navy/gold print, 3/4 sleeves, notch lapel"
    )

    print("Tech Pack:")
    print(json.dumps(result["tech_pack"], indent=2))
    print("\nPrice Quote (₦):")
    print(json.dumps(result["price_quote"], indent=2))
    print("\nFabric Estimate:")
    print(json.dumps(result["fabric_estimate"], indent=2))

    order = {
        "client_name": "Aisha Mohammed",
        "garment": "Corporate Ankara Blazer",
        "size": "14",
        "fabric": "Ankara Navy/Gold",
        "deadline": "July 25, 2024",
        "price_quote": result["price_quote"],
    }
    print("\nOrder Confirmation Message:")
    print(copilot.generate_order_summary(order))
