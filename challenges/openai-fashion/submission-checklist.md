# OpenAI Fashion — Submission Checklist

## Pre-Submission (T-24h)
- [ ] `make eval CHALLENGE=openai-fashion PROFILE=safe` passes with no errors
- [ ] `python -m fashion.agent` runs in stub mode (no API key needed)
- [ ] `python -m fashion.pattern_math` generates SVG in `/tmp/pattern_demo.svg`
- [ ] Frontend builds: `cd frontend && npm run build` succeeds
- [ ] Service Worker registered and caching confirmed in Chrome DevTools

## Core Features Verified
- [ ] AI Tutor: text Q&A returns teaching response with skill_tags
- [ ] AI Tutor: image upload triggers pattern + sewing steps output
- [ ] Skill Tracker: badges awarded after mastery sessions
- [ ] Co-pilot: tech pack JSON generated from description
- [ ] Co-pilot: price quote calculated with correct formula
- [ ] Gallery: 8 mock designs visible, search works, likes work
- [ ] Offline Queue: requests queue when offline, flush when online
- [ ] Pattern SVG: bodice, skirt, trouser patterns render correctly

## Codex Demo Recording
- [ ] Screen recording of Codex generating `pattern_math.py` functions
- [ ] GPT-5.6 explaining the tailoring concept while Codex generates code
- [ ] Recording is ≤ 3 minutes, narrated

## Benchmark Artifacts
- [ ] `benchmarks/openai-fashion_safe_*.json` committed
- [ ] `benchmarks/openai-fashion_aggressive_*.json` committed
- [ ] Quality score ≥ 0.90 confirmed
- [ ] Reliability ≥ 0.99 confirmed

## Submission Package
- [ ] `submissions/assets/technical-writeup.md` filled (fashion section)
- [ ] Demo video recorded (2 minutes max)
- [ ] Video shows: tutor teaching, badge earned, tech pack generated, offline queue
- [ ] Architecture diagram updated with fashion app layers

## Story / Copy
- [ ] One-sentence pitch: "Aku teaches tailoring with AI that works even when internet doesn't"
- [ ] Problem statement: skills gap in $300B fashion/tailoring industry
- [ ] User persona: Lagos tailor, fashion student in Accra
- [ ] Codex + GPT-5.6 roles clearly explained in writeup
- [ ] Offline-first section in writeup

## Final (T-1h)
- [ ] Re-run `make eval CHALLENGE=openai-fashion PROFILE=safe`
- [ ] Frontend deployed (Vercel / Netlify) or local demo ready
- [ ] All links in submission form tested
- [ ] Team members listed
- [ ] Repo is public
- [ ] Submission form submitted before **July 21 at 5:00 PM PT**
