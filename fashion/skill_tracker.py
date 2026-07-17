"""
Skill Tracker
=============
Tracks learner progress through tailoring and fashion skills.
Awards badges when a skill reaches mastery level.

Skills are organized into levels:
  - Beginner    : basic sewing, seams, hand stitches
  - Intermediate: darts, zippers, sleeves, collars
  - Advanced    : tailored suits, couture finishes, pattern drafting
  - Master      : business, teaching, innovation

Usage
-----
    from fashion.skill_tracker import SkillTracker

    tracker = SkillTracker(learner_id="tailor-001")
    tracker.log_skill("invisible-zipper", session_id="s1")
    tracker.log_skill("invisible-zipper", session_id="s2")
    tracker.log_skill("invisible-zipper", session_id="s3")  # → badge awarded

    print(tracker.progress_summary())
    print(tracker.get_badges())
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Skill catalogue
# ---------------------------------------------------------------------------

SKILL_CATALOGUE: dict[str, dict] = {
    # ── Beginner ────────────────────────────────────────────────────────────
    "hand-stitching": {
        "name": "Hand Stitching",
        "level": "Beginner",
        "mastery_sessions": 2,
        "description": "Running stitch, backstitch, slip stitch",
        "badge": "🧵 Needle Ninja",
    },
    "seam-finishing": {
        "name": "Seam Finishing",
        "level": "Beginner",
        "mastery_sessions": 2,
        "description": "Zigzag, overcast, Hong Kong seam",
        "badge": "✂️ Clean Edge",
    },
    "pressing": {
        "name": "Pressing Technique",
        "level": "Beginner",
        "mastery_sessions": 2,
        "description": "Steam pressing, pressing cloths, setting seams",
        "badge": "♨️ Press Master",
    },
    "straight-stitch": {
        "name": "Straight Machine Stitch",
        "level": "Beginner",
        "mastery_sessions": 2,
        "description": "Machine tension, stitch length, seam allowances",
        "badge": "🎯 Straight Shooter",
    },
    # ── Intermediate ────────────────────────────────────────────────────────
    "dart": {
        "name": "Darts",
        "level": "Intermediate",
        "mastery_sessions": 3,
        "description": "Straight, curved, French darts",
        "badge": "💎 Dart Artist",
    },
    "bust-dart": {
        "name": "Bust Dart",
        "level": "Intermediate",
        "mastery_sessions": 3,
        "description": "Bust dart manipulation and fitting",
        "badge": "💎 Dart Artist",
    },
    "waist-dart": {
        "name": "Waist Dart",
        "level": "Intermediate",
        "mastery_sessions": 2,
        "description": "Waist shaping darts",
        "badge": "💎 Dart Artist",
    },
    "invisible-zipper": {
        "name": "Invisible Zipper",
        "level": "Intermediate",
        "mastery_sessions": 3,
        "description": "Hidden zipper installation",
        "badge": "🔒 Zipper Pro",
    },
    "zipper-installation": {
        "name": "Zipper Installation",
        "level": "Intermediate",
        "mastery_sessions": 3,
        "description": "All zipper types",
        "badge": "🔒 Zipper Pro",
    },
    "sleeve-setting": {
        "name": "Setting Sleeves",
        "level": "Intermediate",
        "mastery_sessions": 4,
        "description": "Easing and setting in sleeves",
        "badge": "💪 Sleeve Setter",
    },
    "collar": {
        "name": "Collar Construction",
        "level": "Intermediate",
        "mastery_sessions": 4,
        "description": "Flat collar, shirt collar, stand collar",
        "badge": "👔 Collar King",
    },
    "waistband": {
        "name": "Waistband",
        "level": "Intermediate",
        "mastery_sessions": 2,
        "description": "Waistband application and interfacing",
        "badge": "🏅 Band Boss",
    },
    "ankara-finishing": {
        "name": "Ankara Finishing",
        "level": "Intermediate",
        "mastery_sessions": 3,
        "description": "Working with and finishing Ankara fabric",
        "badge": "🌍 Ankara Expert",
    },
    # ── Advanced ────────────────────────────────────────────────────────────
    "pattern-drafting": {
        "name": "Pattern Drafting",
        "level": "Advanced",
        "mastery_sessions": 5,
        "description": "Drafting bodice, skirt, trouser blocks",
        "badge": "📐 Pattern Master",
    },
    "tailored-jacket": {
        "name": "Tailored Jacket",
        "level": "Advanced",
        "mastery_sessions": 6,
        "description": "Full jacket construction with lining and pad stitching",
        "badge": "🏆 Jacket Artisan",
    },
    "lining": {
        "name": "Lining",
        "level": "Advanced",
        "mastery_sessions": 4,
        "description": "Full and partial lining techniques",
        "badge": "🌟 Inner Beauty",
    },
    "buba-sokoto": {
        "name": "Buba & Sokoto",
        "level": "Advanced",
        "mastery_sessions": 4,
        "description": "Traditional Nigerian two-piece construction",
        "badge": "👑 Heritage Tailor",
    },
    # ── Master ──────────────────────────────────────────────────────────────
    "tech-pack": {
        "name": "Tech Pack Creation",
        "level": "Master",
        "mastery_sessions": 3,
        "description": "Professional technical specification documents",
        "badge": "📋 Tech Pack Pro",
    },
    "garment-math": {
        "name": "Garment Mathematics",
        "level": "Master",
        "mastery_sessions": 4,
        "description": "Pattern math, grading, and scaling",
        "badge": "🧮 Math Maestro",
    },
}

LEVEL_ORDER = ["Beginner", "Intermediate", "Advanced", "Master"]

LEVEL_THRESHOLDS = {
    "Beginner": 3,       # 3 beginner skills to unlock Intermediate
    "Intermediate": 5,   # 5 intermediate skills to unlock Advanced
    "Advanced": 4,       # 4 advanced skills to unlock Master
}


# ---------------------------------------------------------------------------
# Tracker
# ---------------------------------------------------------------------------

@dataclass
class SkillTracker:
    """
    Tracks an individual learner's skill exposure and mastery.

    Parameters
    ----------
    learner_id  : unique identifier for the learner
    persist_path: if set, auto-saves/loads progress from this JSON file
    """
    learner_id: str
    persist_path: str | None = None
    _skill_log: dict[str, list[str]] = field(default_factory=dict)  # skill → [session_ids]
    _badges: list[str] = field(default_factory=list)
    _unlocked_levels: set[str] = field(default_factory=lambda: {"Beginner"})

    def __post_init__(self) -> None:
        if self.persist_path:
            self._load()

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def log_skill(self, skill_tag: str, session_id: str | None = None) -> dict[str, Any]:
        """
        Record that a learner practised *skill_tag* in a session.

        Parameters
        ----------
        skill_tag  : skill identifier (must be in SKILL_CATALOGUE or will be added dynamically)
        session_id : optional session identifier for deduplication

        Returns
        -------
        dict with:
          skill       : normalized skill tag
          sessions    : total sessions for this skill
          mastered    : bool
          new_badge   : badge name if just earned, else None
          level_up    : new level if unlocked, else None
        """
        skill_tag = skill_tag.lower().strip()
        sid = session_id or f"auto-{int(time.time())}"

        if skill_tag not in self._skill_log:
            self._skill_log[skill_tag] = []

        # Deduplicate sessions
        if sid not in self._skill_log[skill_tag]:
            self._skill_log[skill_tag].append(sid)

        sessions = len(self._skill_log[skill_tag])
        mastery = self._mastery_threshold(skill_tag)
        mastered = sessions >= mastery

        new_badge = None
        if mastered:
            new_badge = self._award_badge(skill_tag)

        level_up = self._check_level_up()

        if self.persist_path:
            self._save()

        return {
            "skill": skill_tag,
            "sessions": sessions,
            "mastery_required": mastery,
            "mastered": mastered,
            "new_badge": new_badge,
            "level_up": level_up,
        }

    def log_skills_from_tags(self, tags: list[str], session_id: str | None = None) -> list[dict]:
        """Log multiple skill tags at once (from agent response skill_tags)."""
        results = []
        for tag in tags:
            results.append(self.log_skill(tag, session_id=session_id))
        return results

    def get_badges(self) -> list[str]:
        """Return all earned badges."""
        return list(self._badges)

    def progress_summary(self) -> dict[str, Any]:
        """
        Full progress summary for a learner.

        Returns
        -------
        dict with levels, skills, badges, overall progress percentage
        """
        by_level: dict[str, list[dict]] = {lvl: [] for lvl in LEVEL_ORDER}

        for skill_tag, sessions in self._skill_log.items():
            info = SKILL_CATALOGUE.get(skill_tag, {
                "name": skill_tag.replace("-", " ").title(),
                "level": "Beginner",
                "mastery_sessions": 3,
                "description": "Custom skill",
                "badge": "⭐ Explorer",
            })
            mastery = self._mastery_threshold(skill_tag)
            mastered = len(sessions) >= mastery
            level = info["level"]
            if level in by_level:
                by_level[level].append({
                    "tag": skill_tag,
                    "name": info["name"],
                    "sessions": len(sessions),
                    "mastery_required": mastery,
                    "mastered": mastered,
                    "progress_pct": min(100, round(len(sessions) / mastery * 100)),
                })

        total_skills = len(self._skill_log)
        mastered_count = sum(
            1 for tag, sessions in self._skill_log.items()
            if len(sessions) >= self._mastery_threshold(tag)
        )
        overall_pct = round(mastered_count / max(total_skills, 1) * 100)

        return {
            "learner_id": self.learner_id,
            "unlocked_levels": sorted(self._unlocked_levels),
            "badges": self._badges,
            "badge_count": len(self._badges),
            "total_skills_practiced": total_skills,
            "skills_mastered": mastered_count,
            "overall_mastery_pct": overall_pct,
            "skills_by_level": by_level,
        }

    def next_recommended_skills(self, limit: int = 3) -> list[dict]:
        """
        Suggest the next skills to focus on, based on current progress.
        Prioritises skills close to mastery in unlocked levels.
        """
        suggestions: list[tuple[int, str, dict]] = []

        for tag, info in SKILL_CATALOGUE.items():
            if info["level"] not in self._unlocked_levels:
                continue
            sessions = len(self._skill_log.get(tag, []))
            mastery = info["mastery_sessions"]
            if sessions >= mastery:
                continue   # already mastered
            gap = mastery - sessions
            suggestions.append((gap, tag, info))

        suggestions.sort(key=lambda x: x[0])

        return [
            {
                "tag": tag,
                "name": info["name"],
                "level": info["level"],
                "sessions_remaining": gap,
                "description": info["description"],
            }
            for gap, tag, info in suggestions[:limit]
        ]

    # -----------------------------------------------------------------------
    # Internal
    # -----------------------------------------------------------------------

    def _mastery_threshold(self, skill_tag: str) -> int:
        return SKILL_CATALOGUE.get(skill_tag, {}).get("mastery_sessions", 3)

    def _award_badge(self, skill_tag: str) -> str | None:
        badge = SKILL_CATALOGUE.get(skill_tag, {}).get("badge")
        if badge and badge not in self._badges:
            self._badges.append(badge)
            return badge
        return None

    def _check_level_up(self) -> str | None:
        for i, level in enumerate(LEVEL_ORDER[:-1]):
            next_level = LEVEL_ORDER[i + 1]
            if next_level in self._unlocked_levels:
                continue
            threshold = LEVEL_THRESHOLDS.get(level, 999)
            mastered_at_level = sum(
                1 for tag, sessions in self._skill_log.items()
                if SKILL_CATALOGUE.get(tag, {}).get("level") == level
                and len(sessions) >= self._mastery_threshold(tag)
            )
            if mastered_at_level >= threshold:
                self._unlocked_levels.add(next_level)
                return next_level
        return None

    def _save(self) -> None:
        data = {
            "learner_id": self.learner_id,
            "skill_log": self._skill_log,
            "badges": self._badges,
            "unlocked_levels": list(self._unlocked_levels),
        }
        Path(self.persist_path).write_text(json.dumps(data, indent=2))  # type: ignore[arg-type]

    def _load(self) -> None:
        path = Path(self.persist_path)  # type: ignore[arg-type]
        if not path.exists():
            return
        data = json.loads(path.read_text())
        self._skill_log = data.get("skill_log", {})
        self._badges = data.get("badges", [])
        self._unlocked_levels = set(data.get("unlocked_levels", ["Beginner"]))


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tracker = SkillTracker(learner_id="demo-tailor")

    print("=== Skill Tracker Demo ===\n")

    # Simulate 3 sessions on invisible zipper
    for i in range(3):
        result = tracker.log_skill("invisible-zipper", session_id=f"session-{i}")
        print(f"Session {i+1}: {result}")

    print()
    print("Badges earned:", tracker.get_badges())
    print()

    # Log a few more skills
    tracker.log_skill("dart", session_id="s1")
    tracker.log_skill("dart", session_id="s2")
    tracker.log_skill("dart", session_id="s3")
    tracker.log_skill("pressing", session_id="p1")
    tracker.log_skill("pressing", session_id="p2")

    summary = tracker.progress_summary()
    print("Progress Summary:")
    print(f"  Mastered: {summary['skills_mastered']} / {summary['total_skills_practiced']} skills")
    print(f"  Badges:   {summary['badges']}")
    print(f"  Levels:   {summary['unlocked_levels']}")

    print("\nNext recommended:")
    for rec in tracker.next_recommended_skills():
        print(f"  • {rec['name']} ({rec['level']}) — {rec['sessions_remaining']} session(s) to mastery")
