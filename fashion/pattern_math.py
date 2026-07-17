"""
Pattern Math — Codex-Generated Pattern Calculation Engine
==========================================================
This module demonstrates **Codex working side-by-side** with GPT-5.6:
GPT-5.6 handles the tailoring logic and teaching; Codex generates these
precise mathematical functions and SVG output.

All measurements in centimetres unless otherwise stated.

Usage
-----
    from fashion.pattern_math import PatternCalculator

    calc = PatternCalculator(bust=88, waist=68, hip=94, back_length=40)
    bodice = calc.bodice_block()
    skirt  = calc.straight_skirt()
    svg    = calc.to_svg([bodice, skirt])
    print(svg)
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Point(NamedTuple):
    x: float
    y: float

    def __add__(self, other: "Point") -> "Point":  # type: ignore[override]
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":  # type: ignore[override]
        return Point(self.x - other.x, self.y - other.y)


@dataclass
class PatternPiece:
    """A single pattern piece with a name, outline points, and grain line."""
    name: str
    points: list[Point]
    grain_line: tuple[Point, Point] | None = None
    labels: dict[str, Point] = field(default_factory=dict)
    seam_allowance_cm: float = 1.5

    def bounding_box(self) -> tuple[float, float, float, float]:
        """Return (min_x, min_y, max_x, max_y)."""
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return min(xs), min(ys), max(xs), max(ys)

    def width(self) -> float:
        bb = self.bounding_box()
        return bb[2] - bb[0]

    def height(self) -> float:
        bb = self.bounding_box()
        return bb[3] - bb[1]


# ---------------------------------------------------------------------------
# Main calculator — Codex-generated pattern math
# ---------------------------------------------------------------------------

@dataclass
class PatternCalculator:
    """
    Generates garment pattern blocks from body measurements.

    Parameters
    ----------
    bust        : full bust circumference in cm
    waist       : full waist circumference in cm
    hip         : full hip circumference in cm
    back_length : nape of neck to waist in cm
    shoulder    : shoulder width in cm (across back)
    inseam      : inseam length for trousers in cm (optional)
    ease        : ease to add to bust (cm); default 4 cm for fitted
    """
    bust: float
    waist: float
    hip: float
    back_length: float
    shoulder: float = 12.0
    inseam: float = 75.0
    ease: float = 4.0

    # -----------------------------------------------------------------------
    # Core measurements (computed)
    # -----------------------------------------------------------------------

    @property
    def half_bust(self) -> float:
        """Half bust + ease."""
        return (self.bust + self.ease) / 2

    @property
    def half_waist(self) -> float:
        return self.waist / 2

    @property
    def half_hip(self) -> float:
        return self.hip / 2

    @property
    def bust_dart_intake(self) -> float:
        """Total dart intake = difference between half-bust and half-waist."""
        return max(0.0, self.half_bust - self.half_waist)

    @property
    def side_dart(self) -> float:
        """Dart distributed to side seam."""
        return self.bust_dart_intake / 2

    # -----------------------------------------------------------------------
    # Pattern blocks
    # -----------------------------------------------------------------------

    def bodice_block(self) -> PatternPiece:
        """
        Draft a basic fitted bodice block (back piece).

        Drafted on a right-angle grid:
        - Origin A at top-left (centre back neck)
        - X axis = width (towards side seam)
        - Y axis = length (towards waist)
        """
        hb = self.half_bust / 2          # quarter bust
        hw = self.half_waist / 2         # quarter waist
        bl = self.back_length
        sh = self.shoulder
        armhole_depth = bl * 0.4         # ~40% of back length

        a = Point(0, 0)                  # centre back neck
        b = Point(sh, 0)                 # shoulder point
        e = Point(hb, armhole_depth)     # armhole side
        d = Point(hw + self.side_dart, bl)  # side seam waist
        c = Point(0, bl)                 # centre back waist

        # Armhole control point for cubic bezier (approximate with midpoint)
        armhole_ctrl = Point((b.x + e.x) / 2 + 1, (b.y + e.y) / 2 - 1)

        points = [a, b, armhole_ctrl, e, d, c, a]

        grain = (Point(0.5, bl * 0.2), Point(0.5, bl * 0.8))

        labels = {
            "CB Neck": a,
            "Shoulder": b,
            "Armhole": e,
            "Side Waist": d,
            "CB Waist": c,
        }

        return PatternPiece(
            name="Bodice Back",
            points=points,
            grain_line=grain,
            labels=labels,
        )

    def front_bodice_block(self) -> PatternPiece:
        """
        Draft front bodice block with bust dart.

        The bust dart is positioned at the side seam,
        pointing toward the bust point.
        """
        hb = self.half_bust / 2 + 0.5   # front is slightly wider
        hw = self.half_waist / 2
        bl = self.back_length + 1.5      # front is slightly longer
        sh = self.shoulder - 0.5
        armhole_depth = bl * 0.4

        # Bust point (approximately)
        bust_pt = Point(hb * 0.6, armhole_depth * 0.8)

        a = Point(0, 0)                  # centre front neck
        b = Point(sh, 0)                 # shoulder point
        e = Point(hb, armhole_depth)     # armhole
        # Dart legs on side seam
        dart_width = self.bust_dart_intake * 0.6
        dart_top = Point(hb, armhole_depth + 3)
        dart_bottom = Point(hb, armhole_depth + 3 + dart_width)
        d = Point(hw, bl)                # side seam waist
        c = Point(0, bl)                 # centre front waist

        points = [a, b, e, dart_top, bust_pt, dart_bottom, d, c, a]

        grain = (Point(0.5, bl * 0.2), Point(0.5, bl * 0.8))

        labels = {
            "CF Neck": a,
            "Shoulder": b,
            "Armhole": e,
            "Bust Point": bust_pt,
            "Dart Top": dart_top,
            "Dart Bottom": dart_bottom,
            "CF Waist": c,
        }

        return PatternPiece(
            name="Bodice Front",
            points=points,
            grain_line=grain,
            labels=labels,
        )

    def straight_skirt(self, length_cm: float = 60.0) -> PatternPiece:
        """
        Draft a basic straight skirt back panel.

        Parameters
        ----------
        length_cm : skirt length from waist to hem
        """
        hw = self.half_waist / 2
        hh = self.half_hip / 2
        hip_depth = 20.0    # hip level is ~20 cm below waist

        dart_intake = max(0.0, hh - hw)
        dart_pos = hw * 0.5  # dart at half of back width

        a = Point(0, 0)             # centre back waist
        b = Point(hw, 0)            # side waist (before dart)
        c = Point(hh, hip_depth)    # side hip
        d = Point(hh, length_cm)    # side hem
        e = Point(0, length_cm)     # centre back hem

        # Waist dart
        dart_tip = Point(dart_pos, hip_depth - 5)
        dart_left = Point(dart_pos - dart_intake / 4, 0)
        dart_right = Point(dart_pos + dart_intake / 4, 0)

        points = [a, dart_left, dart_tip, dart_right, b, c, d, e, a]

        grain = (Point(hh * 0.5, length_cm * 0.1), Point(hh * 0.5, length_cm * 0.9))

        labels = {
            "CB Waist": a,
            "Side Waist": b,
            "Side Hip": c,
            "Side Hem": d,
            "CB Hem": e,
            "Dart Tip": dart_tip,
        }

        return PatternPiece(
            name="Straight Skirt Back",
            points=points,
            grain_line=grain,
            labels=labels,
            seam_allowance_cm=1.5,
        )

    def trouser_block(self) -> list[PatternPiece]:
        """
        Draft basic trouser block — front and back panels.

        Returns a list with [front, back] PatternPiece objects.
        """
        hw = self.half_waist / 2
        hh = self.half_hip / 2
        rise = 28.0              # body rise (fork to waist)
        inseam = self.inseam

        # Front panel
        crotch_ext = hh * 0.04  # small front crotch extension
        front_pts = [
            Point(0, 0),             # CF waist
            Point(hw - 0.5, 0),      # side waist
            Point(hh - 0.5, rise),   # side hip level
            Point(hh - 0.5 + crotch_ext, rise + inseam),  # side ankle
            Point(crotch_ext, rise + inseam),              # inside ankle
            Point(-crotch_ext, rise + 5),                  # fork
            Point(0, 0),
        ]
        front = PatternPiece(
            name="Trouser Front",
            points=front_pts,
            grain_line=(
                Point(hh * 0.2, rise * 0.1),
                Point(hh * 0.2, (rise + inseam) * 0.9),
            ),
        )

        # Back panel (wider at seat)
        seat_ext = hh * 0.12
        back_pts = [
            Point(-0.5, 0),
            Point(hw + 1, 0),
            Point(hh + seat_ext * 0.5, rise),
            Point(hh + seat_ext * 0.5, rise + inseam),
            Point(seat_ext * 0.5, rise + inseam),
            Point(-seat_ext, rise + 5),
            Point(-0.5, 0),
        ]
        back = PatternPiece(
            name="Trouser Back",
            points=back_pts,
            grain_line=(
                Point(hh * 0.4, rise * 0.1),
                Point(hh * 0.4, (rise + inseam) * 0.9),
            ),
        )

        return [front, back]

    def fabric_estimate(self, pieces: list[PatternPiece], fabric_width_cm: float = 114.0) -> dict:
        """
        Estimate fabric yardage for a list of pattern pieces.

        Uses a simple bounding-box packing heuristic (assumes 15% layout waste).

        Parameters
        ----------
        pieces          : list of PatternPiece objects
        fabric_width_cm : usable fabric width (114 cm / 45 inch is common)

        Returns
        -------
        dict with total_cm, total_yards, total_metres
        """
        total_area = sum(p.width() * p.height() for p in pieces)
        # Account for 2× (fold) and 15% waste
        raw_length = (total_area * 2 * 1.15) / fabric_width_cm
        # Round up to nearest 10 cm
        length_cm = math.ceil(raw_length / 10) * 10

        return {
            "total_cm": length_cm,
            "total_metres": round(length_cm / 100, 2),
            "total_yards": round(length_cm / 91.44, 2),
            "fabric_width_cm": fabric_width_cm,
            "pieces_count": len(pieces),
            "note": "Add 10% for print matching on patterned fabrics (e.g. Ankara)",
        }

    # -----------------------------------------------------------------------
    # SVG output — Codex-generated
    # -----------------------------------------------------------------------

    def to_svg(
        self,
        pieces: list[PatternPiece],
        scale: float = 4.0,
        padding: float = 20.0,
    ) -> str:
        """
        Convert a list of PatternPiece objects to a single SVG string.

        Parameters
        ----------
        pieces  : list of PatternPiece objects
        scale   : pixels per cm (default 4 → 1 cm = 4 px)
        padding : padding between pieces in pixels

        Returns
        -------
        SVG string suitable for saving as .svg or embedding in HTML
        """
        # Layout pieces side by side
        x_offset = padding
        y_offset = padding
        max_height = 0.0
        svg_pieces: list[str] = []
        row_width = 0.0

        for piece in pieces:
            bb = piece.bounding_box()
            piece_w = (bb[2] - bb[0]) * scale
            piece_h = (bb[3] - bb[1]) * scale

            # Translate points to SVG coordinates
            def tx(x: float) -> float:
                return (x - bb[0]) * scale + x_offset

            def ty(y: float) -> float:
                return (y - bb[1]) * scale + y_offset

            # Build path
            path_d = " ".join(
                f"{'M' if i == 0 else 'L'} {tx(p.x):.1f} {ty(p.y):.1f}"
                for i, p in enumerate(piece.points)
            ) + " Z"

            piece_svg = [
                f'  <g class="pattern-piece" id="{_svg_id(piece.name)}">',
                f'    <path d="{path_d}" fill="none" stroke="#1a1a2e" stroke-width="1.5"/>',
            ]

            # Grain line
            if piece.grain_line:
                gl = piece.grain_line
                piece_svg.append(
                    f'    <line x1="{tx(gl[0].x):.1f}" y1="{ty(gl[0].y):.1f}" '
                    f'x2="{tx(gl[1].x):.1f}" y2="{ty(gl[1].y):.1f}" '
                    f'stroke="#e63946" stroke-width="1" stroke-dasharray="4,2" '
                    f'marker-end="url(#arrow)"/>'
                )

            # Labels
            for label, pt in piece.labels.items():
                piece_svg.append(
                    f'    <text x="{tx(pt.x):.1f}" y="{ty(pt.y) - 3:.1f}" '
                    f'font-size="6" fill="#457b9d" text-anchor="middle">{label}</text>'
                )

            # Piece name
            cx = x_offset + piece_w / 2
            cy = y_offset + piece_h / 2
            piece_svg.append(
                f'    <text x="{cx:.1f}" y="{cy:.1f}" font-size="8" '
                f'fill="#1d3557" text-anchor="middle" font-weight="bold">{piece.name}</text>'
            )
            piece_svg.append("  </g>")
            svg_pieces.extend(piece_svg)

            max_height = max(max_height, piece_h)
            x_offset += piece_w + padding
            row_width = x_offset

        total_w = row_width + padding
        total_h = max_height + y_offset + padding

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w:.0f}" height="{total_h:.0f}" '
            f'viewBox="0 0 {total_w:.0f} {total_h:.0f}">',
            "  <defs>",
            "    <marker id='arrow' markerWidth='6' markerHeight='6' refX='3' refY='3' orient='auto'>",
            "      <path d='M0,0 L6,3 L0,6 Z' fill='#e63946'/>",
            "    </marker>",
            "  </defs>",
            f'  <rect width="{total_w:.0f}" height="{total_h:.0f}" fill="#f8f9fa"/>',
        ]
        svg.extend(svg_pieces)
        svg.append("</svg>")
        return "\n".join(svg)


def _svg_id(name: str) -> str:
    return name.lower().replace(" ", "-")


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    calc = PatternCalculator(bust=88, waist=68, hip=94, back_length=40)

    bodice = calc.bodice_block()
    front = calc.front_bodice_block()
    skirt = calc.straight_skirt(length_cm=65)
    trousers = calc.trouser_block()

    estimate = calc.fabric_estimate([bodice, front, skirt])

    print("=== Pattern Calculator Demo ===\n")
    print(f"Bodice Back  — {bodice.width():.1f} cm × {bodice.height():.1f} cm")
    print(f"Bodice Front — {front.width():.1f} cm × {front.height():.1f} cm")
    print(f"Straight Skirt — {skirt.width():.1f} cm × {skirt.height():.1f} cm")
    print(f"Bust dart intake: {calc.bust_dart_intake:.1f} cm")
    print()
    print("Fabric estimate:")
    for k, v in estimate.items():
        print(f"  {k}: {v}")

    svg = calc.to_svg([bodice, front, skirt])
    out = "/tmp/pattern_demo.svg"
    with open(out, "w") as f:
        f.write(svg)
    print(f"\nSVG pattern saved to {out}")
