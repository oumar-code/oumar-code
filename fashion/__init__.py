"""
Fashion AI — OpenAI Build Week
================================
AI-powered tailoring and fashion skills app targeting tailors,
fashion students, and learners in low-resource settings.

Sub-modules
-----------
agent         : GPT-5.6 Fashion Tutor Agent (multi-turn, teaching-mode)
pattern_math  : Codex-generated pattern calculation & SVG output
skill_tracker : Skill progress tracking and badge system
copilot       : Tailor Co-pilot — tech pack, fabric estimate, price quote
gallery       : Mock community gallery
offline_queue : Offline-first request queue (sync when connectivity returns)
"""

from fashion.agent import FashionTutorAgent
from fashion.pattern_math import PatternCalculator
from fashion.skill_tracker import SkillTracker
from fashion.copilot import TailorCopilot
from fashion.gallery import CommunityGallery
from fashion.offline_queue import OfflineQueue

__all__ = [
    "FashionTutorAgent",
    "PatternCalculator",
    "SkillTracker",
    "TailorCopilot",
    "CommunityGallery",
    "OfflineQueue",
]
