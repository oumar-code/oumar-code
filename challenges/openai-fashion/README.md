# Challenge: OpenAI Build Week — AI Fashion & Tailoring Skills App

## Overview

**Aku Fashion** is an AI-powered tailoring and fashion skills app for tailors,
fashion students, and learners — especially in low-resource settings across Africa.

Built for **OpenAI Build Week** (July 13–21, 2025), this project demonstrates
GPT-5.6 and Codex working **side-by-side**: GPT-5.6 handles teaching, fashion
logic, and QA; Codex generates pattern math functions and SVG output.

## The Three Pillars

| Pillar | What It Does |
|---|---|
| **AI Fashion Tutor** | GPT-5.6 agent that teaches tailoring step-by-step; badge system for skill mastery |
| **Tailor Co-pilot** | Tech pack, fabric estimate, and price quote from a garment description or inspo photo |
| **Design Prototyper** | Type a description → Codex generates SVG pattern pieces and cutting guides |

## Judge Criteria Mapping

| Judge Criterion | How We Address It | Target |
|---|---|---|
| Codex actually building | `pattern_math.py` — Codex-generated pattern functions | Demo recording shows Codex writing functions live |
| Agent side-by-side | GPT-5.6 teaches + Codex generates; distinct roles, single workflow | Full agent loop in demo |
| Real problem | Upskilling tailors + fashion students in low-resource/offline settings | Clear user story + offline-first architecture |
| Quality | Structured tech packs, precise pattern math, rich skill tracking | quality_score ≥ 0.90 |
| Reliability | Offline-first; falls back gracefully; never crashes demo | reliability ≥ 0.99 |

## Run Instructions

```bash
# Tutor agent demo (stub mode — no API key needed)
python -m fashion.agent

# Pattern math demo + SVG output
python -m fashion.pattern_math

# Skill tracker demo
python -m fashion.skill_tracker

# Tailor co-pilot demo
python -m fashion.copilot

# Community gallery demo
python -m fashion.gallery

# Offline queue demo
python -m fashion.offline_queue

# Full pipeline eval
make eval CHALLENGE=openai-fashion PROFILE=safe

# Next.js frontend
cd frontend && npm install && npm run dev
```

## Architecture

```
User (browser / PWA)
        │
        ▼
  Next.js 14 Frontend (Tailwind CSS)
  ├── /tutor     → AI Fashion Tutor chat
  ├── /copilot   → Tech pack + price quote
  ├── /design    → SVG pattern generator
  ├── /skills    → Skill tracker + badges
  └── /gallery   → Community designs
        │
  Service Worker (offline cache + queue)
        │
        ▼
  API Routes (Next.js / FastAPI)
  ├── GPT-5.6   — teaching, vision analysis, fashion QA
  └── Codex     — pattern math, SVG generation, boilerplate
        │
        ▼
  Python Fashion Package (fashion/)
  ├── agent.py          FashionTutorAgent
  ├── pattern_math.py   PatternCalculator + SVG
  ├── skill_tracker.py  SkillTracker + badges
  ├── copilot.py        TailorCopilot
  ├── gallery.py        CommunityGallery
  └── offline_queue.py  OfflineQueue
```

## Key Differentiators

1. **Domain-specific**: Built for a $300B+ underserved industry (global fashion/tailoring)
2. **Offline-first**: Service Worker + queue — works where internet is unreliable
3. **Real users**: Tailors and fashion students in Nigeria, Ghana, Kenya, and across Africa
4. **Codex + GPT-5.6 clearly separated**: Codex = generative math/code; GPT-5.6 = teaching/QA
5. **Skill progression**: Badge system that motivates learning and tracks mastery

## References
- Agent: `fashion/agent.py`
- Pattern Math (Codex demo): `fashion/pattern_math.py`
- Skill Tracker: `fashion/skill_tracker.py`
- Co-pilot: `fashion/copilot.py`
- Gallery: `fashion/gallery.py`
- Offline Queue: `fashion/offline_queue.py`
- Frontend: `frontend/`
- Challenge config: `challenges/openai-fashion/`
