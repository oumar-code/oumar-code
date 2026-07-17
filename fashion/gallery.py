"""
Community Gallery
=================
Mock community gallery for sharing fashion designs and getting feedback.
In production this would be backed by a database; here it uses an in-memory
store with optional JSON file persistence for demo purposes.

Usage
-----
    from fashion.gallery import CommunityGallery

    gallery = CommunityGallery()
    gallery.add_design(
        title="Modern Buba & Sokoto",
        designer="Fatima Aliyu",
        description="Corporate-ready buba with tapered sokoto",
        tags=["buba-sokoto", "corporate", "ankara"],
        image_url="https://example.com/design.jpg",
    )
    print(gallery.list_designs())
    print(gallery.trending())
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Design:
    id: str
    title: str
    designer: str
    description: str
    tags: list[str]
    image_url: str
    created_at: float
    likes: int = 0
    comments: list[dict] = field(default_factory=list)
    skill_level: str = "Intermediate"
    fabric_type: str = "ankara"


@dataclass
class CommunityGallery:
    """
    Community gallery for fashion designs.

    Parameters
    ----------
    persist_path : optional path to JSON file for persistence
    """
    persist_path: str | None = None
    _designs: dict[str, Design] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.persist_path and Path(self.persist_path).exists():
            self._load()
        elif not self._designs:
            self._seed_mock_data()

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def add_design(
        self,
        title: str,
        designer: str,
        description: str,
        tags: list[str] | None = None,
        image_url: str = "",
        skill_level: str = "Intermediate",
        fabric_type: str = "ankara",
    ) -> Design:
        """Add a new design to the gallery."""
        design = Design(
            id=str(uuid.uuid4())[:8],
            title=title,
            designer=designer,
            description=description,
            tags=tags or [],
            image_url=image_url,
            created_at=time.time(),
            skill_level=skill_level,
            fabric_type=fabric_type,
        )
        self._designs[design.id] = design
        if self.persist_path:
            self._save()
        return design

    def like_design(self, design_id: str) -> int:
        """Like a design. Returns updated like count."""
        if design_id in self._designs:
            self._designs[design_id].likes += 1
            if self.persist_path:
                self._save()
            return self._designs[design_id].likes
        return 0

    def add_comment(self, design_id: str, author: str, text: str) -> dict | None:
        """Add a comment to a design."""
        if design_id not in self._designs:
            return None
        comment = {
            "id": str(uuid.uuid4())[:6],
            "author": author,
            "text": text,
            "timestamp": time.time(),
        }
        self._designs[design_id].comments.append(comment)
        if self.persist_path:
            self._save()
        return comment

    def get_design(self, design_id: str) -> Design | None:
        return self._designs.get(design_id)

    def list_designs(
        self,
        tag: str | None = None,
        skill_level: str | None = None,
        limit: int = 20,
        sort_by: str = "recent",  # "recent" | "popular"
    ) -> list[dict[str, Any]]:
        """
        List designs, optionally filtered by tag or skill level.

        Parameters
        ----------
        tag         : filter by tag
        skill_level : filter by skill level
        limit       : max results
        sort_by     : "recent" or "popular"
        """
        designs = list(self._designs.values())

        if tag:
            designs = [d for d in designs if tag.lower() in [t.lower() for t in d.tags]]
        if skill_level:
            designs = [d for d in designs if d.skill_level.lower() == skill_level.lower()]

        if sort_by == "popular":
            designs.sort(key=lambda d: d.likes, reverse=True)
        else:
            designs.sort(key=lambda d: d.created_at, reverse=True)

        return [_design_to_dict(d) for d in designs[:limit]]

    def trending(self, limit: int = 5) -> list[dict[str, Any]]:
        """Return the most-liked designs."""
        return self.list_designs(limit=limit, sort_by="popular")

    def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Simple keyword search across titles, descriptions, and tags."""
        q = query.lower()
        results = []
        for design in self._designs.values():
            searchable = (
                design.title.lower()
                + " " + design.description.lower()
                + " " + " ".join(design.tags)
            )
            if q in searchable:
                results.append(design)
        results.sort(key=lambda d: d.likes, reverse=True)
        return [_design_to_dict(d) for d in results[:limit]]

    def stats(self) -> dict[str, Any]:
        """Gallery statistics."""
        designs = list(self._designs.values())
        return {
            "total_designs": len(designs),
            "total_likes": sum(d.likes for d in designs),
            "total_comments": sum(len(d.comments) for d in designs),
            "designers": len({d.designer for d in designs}),
            "top_tags": _top_n_tags(designs, 5),
        }

    # -----------------------------------------------------------------------
    # Internal
    # -----------------------------------------------------------------------

    def _seed_mock_data(self) -> None:
        """Populate with realistic mock designs for demo."""
        mock_designs = [
            {
                "title": "Modern Buba & Sokoto",
                "designer": "Fatima Aliyu",
                "description": (
                    "A sleek corporate reinterpretation of the classic buba and sokoto. "
                    "Tailored fit, notch lapel collar on the buba, tapered ankle-length sokoto. "
                    "Perfect for the modern African professional woman."
                ),
                "tags": ["buba-sokoto", "corporate", "ankara", "womens-wear", "tailored"],
                "image_url": "https://placeholder.com/design-1.jpg",
                "skill_level": "Advanced",
                "fabric_type": "ankara",
                "likes": 47,
            },
            {
                "title": "Kente Wrap Dress",
                "designer": "Kofi Mensah",
                "description": (
                    "Floor-length wrap dress in authentic Ghanaian kente cloth. "
                    "V-neckline, flutter sleeves, adjustable tie waist. "
                    "Demonstrates advanced kente handling techniques."
                ),
                "tags": ["kente", "wrap-dress", "ghana", "floor-length", "occasion-wear"],
                "image_url": "https://placeholder.com/design-2.jpg",
                "skill_level": "Advanced",
                "fabric_type": "kente",
                "likes": 62,
            },
            {
                "title": "Ankara Blazer (Structural Padded)",
                "designer": "Chioma Okafor",
                "description": (
                    "Power-shoulder ankara blazer with structured padding. "
                    "Single-breasted, 2-button closure, welt pockets. "
                    "Fully lined in contrast fabric. Demonstrates full tailoring construction."
                ),
                "tags": ["blazer", "ankara", "power-shoulder", "corporate", "complex"],
                "image_url": "https://placeholder.com/design-3.jpg",
                "skill_level": "Advanced",
                "fabric_type": "ankara",
                "likes": 89,
            },
            {
                "title": "Lace Mermaid Evening Gown",
                "designer": "Amina Ibrahim",
                "description": (
                    "Floor-length mermaid gown in Nigerian guipure lace. "
                    "Sweetheart neckline, invisible zipper, godets at knee for flare. "
                    "One of my most challenging pieces — the godets took 3 attempts!"
                ),
                "tags": ["lace", "mermaid", "evening-gown", "godets", "couture"],
                "image_url": "https://placeholder.com/design-4.jpg",
                "skill_level": "Master",
                "fabric_type": "lace",
                "likes": 134,
            },
            {
                "title": "Beginner Pencil Skirt",
                "designer": "Grace Adeyemi",
                "description": (
                    "My very first pencil skirt! Straight cut, invisible zipper at back, "
                    "waistband with interfacing. Learned so much about pressing and darts."
                ),
                "tags": ["pencil-skirt", "beginner", "cotton", "first-project"],
                "image_url": "https://placeholder.com/design-5.jpg",
                "skill_level": "Beginner",
                "fabric_type": "cotton",
                "likes": 28,
            },
            {
                "title": "Aso-oke Senator Agbada",
                "designer": "Babatunde Lawson",
                "description": (
                    "Traditional Nigerian agbada in hand-woven aso-oke. "
                    "Three-piece set: outer agbada, inner buba, sokoto. "
                    "Embroidered neckline and cuffs. Wedding ceremony piece."
                ),
                "tags": ["agbada", "aso-oke", "traditional", "mens-wear", "wedding"],
                "image_url": "https://placeholder.com/design-6.jpg",
                "skill_level": "Master",
                "fabric_type": "aso-oke",
                "likes": 203,
            },
            {
                "title": "Chiffon Ruffle Blouse",
                "designer": "Ngozi Eze",
                "description": (
                    "Flowy chiffon blouse with cascading ruffle front. "
                    "French seams throughout for clean finish. "
                    "Tutorial: the trick is to stay-stitch every edge before cutting chiffon."
                ),
                "tags": ["blouse", "chiffon", "ruffles", "french-seams", "intermediate"],
                "image_url": "https://placeholder.com/design-7.jpg",
                "skill_level": "Intermediate",
                "fabric_type": "chiffon",
                "likes": 41,
            },
            {
                "title": "Ankara Shift Dress",
                "designer": "Aisha Mohammed",
                "description": (
                    "Clean, minimalist shift dress in bold geometric ankara. "
                    "A-line silhouette, round neck, invisible zipper at centre back. "
                    "Great everyday piece and approachable for intermediate sewists."
                ),
                "tags": ["shift-dress", "ankara", "a-line", "everyday-wear", "intermediate"],
                "image_url": "https://placeholder.com/design-8.jpg",
                "skill_level": "Intermediate",
                "fabric_type": "ankara",
                "likes": 56,
            },
        ]

        for i, d in enumerate(mock_designs):
            likes = d.pop("likes", 0)
            design = self.add_design(**d)
            design.likes = likes
            design.created_at = time.time() - (i * 86400)  # stagger timestamps

    def _save(self) -> None:
        data = {
            did: {
                "id": d.id,
                "title": d.title,
                "designer": d.designer,
                "description": d.description,
                "tags": d.tags,
                "image_url": d.image_url,
                "created_at": d.created_at,
                "likes": d.likes,
                "comments": d.comments,
                "skill_level": d.skill_level,
                "fabric_type": d.fabric_type,
            }
            for did, d in self._designs.items()
        }
        Path(self.persist_path).write_text(json.dumps(data, indent=2))  # type: ignore[arg-type]

    def _load(self) -> None:
        raw = json.loads(Path(self.persist_path).read_text())  # type: ignore[arg-type]
        for did, d in raw.items():
            self._designs[did] = Design(**d)


def _design_to_dict(d: Design) -> dict[str, Any]:
    return {
        "id": d.id,
        "title": d.title,
        "designer": d.designer,
        "description": d.description,
        "tags": d.tags,
        "image_url": d.image_url,
        "likes": d.likes,
        "comments_count": len(d.comments),
        "skill_level": d.skill_level,
        "fabric_type": d.fabric_type,
        "created_at": d.created_at,
    }


def _top_n_tags(designs: list[Design], n: int) -> list[dict]:
    counts: dict[str, int] = {}
    for d in designs:
        for tag in d.tags:
            counts[tag] = counts.get(tag, 0) + 1
    sorted_tags = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [{"tag": t, "count": c} for t, c in sorted_tags[:n]]


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    gallery = CommunityGallery()

    print("=== Community Gallery Demo ===\n")
    print("Gallery stats:")
    print(json.dumps(gallery.stats(), indent=2))

    print("\nTrending designs:")
    for d in gallery.trending(3):
        print(f"  {d['likes']:3} ❤  {d['title']} by {d['designer']} [{d['skill_level']}]")

    print("\nSearch 'ankara':")
    for d in gallery.search("ankara", limit=3):
        print(f"  {d['title']} — {d['tags']}")

    # Add a new design
    new = gallery.add_design(
        title="My First Dart Dress",
        designer="Demo User",
        description="Practice project: fitted dress with waist and bust darts",
        tags=["dart", "beginner", "practice"],
        skill_level="Beginner",
    )
    gallery.like_design(new.id)
    gallery.add_comment(new.id, "Aku Tutor", "Great work! Your darts are smooth 🎉")
    print(f"\nAdded: {new.title} (id={new.id})")
