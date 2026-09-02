# 🏆 Hackathon Tracking & Submissions

Comprehensive tracking of all active and completed hackathon submissions with links, status, and key deliverables.

---

## 🔴 ACTIVE BUILD (Currently Focusing On)

### ✂️ OpenAI Build Week — Aku Fashion App
- **Status**: 🔨 **ACTIVELY BUILDING**
- **Repository**: https://github.com/oumar-code/oumar-code
- **Challenge Track**: OpenAI Fashion (`challenges/openai-fashion/`)
- **Duration**: July 13-21, 2025
- **Key Features**:
  - GPT-5.6 Fashion Tutor Agent (multi-turn, offline-first)
  - Codex Pattern Math + SVG renderer
  - Skill Tracker with badge system
  - Tailor Co-pilot (tech pack, price quote)
  - Service Worker for offline caching
  - Next.js 14 + Tailwind CSS frontend
- **Tech Stack**: Python (FastAPI), TypeScript (Next.js), Offline-First
- **Submission Checklist**: `challenges/openai-fashion/submission-checklist.md`
- **Target**: Demonstrate GPT-5.6 + Codex working side-by-side for fashion education in low-resource African settings

**Key Deliverables**:
- ✅ AI Tutor: step-by-step teaching with skill_tags extraction
- ✅ Pattern Generator: measurements → SVG patterns
- ✅ Tech Pack Co-pilot: JSON specs + price quotes
- ✅ Offline Queue: requests queued when offline, synced online
- ⏳ Benchmark artifacts (safe & aggressive profiles)
- ⏳ Demo video (2 min max)
- ⏳ Technical writeup

---

### 🦵 Kaggle — Knee MRI Abnormality Detection
- **Status**: 🔨 **ACTIVELY BUILDING**
- **Repository / Path**: `challenges/kaggle-knee-mri/` (this repo)
- **Challenge Summary**: Develop multimodal ML models to detect 12 clinically important knee abnormalities (ACL, MCL, meniscal tears, OA, effusion, synovitis, Baker's, contusion, fracture). Dataset pairs MRI imaging studies with original radiology reports.
- **Objective**: Maximize macro-averaged ROC-AUC across the 12 targets; produce a reproducible training & inference pipeline and final CSV submission with StudyInstanceUID + confidence scores for each target.
- **Evaluation**: Macro-averaged AUC ROC (average of 12 per-class AUCs).
- **Submission Format**: CSV with header "StudyInstanceUID,ACL,MCL,Medial Meniscus,Lateral Meniscus,Medial OA,Lateral OA,PF OA,Effusion,Synovitis,Baker's,Contusion,Fracture" and a row per test study with confidence scores [0..1].
- **Maintainer**: @oumar-code
- **Duration / Timeline**: Sprint-style: 3-week sprint (EDA & baseline, multimodal, improvements, ensembling).

Key Deliverables & Status:
- [ ] Baseline pipeline: DICOM loader → slice-wise 2D CNN → study-level aggregation → CSV submission
- [ ] Report-only model: fine-tune clinical BERT on radiology reports
- [ ] Multimodal fusion: image + report embeddings
- [ ] Improved models: 3D/2.5D, slice transformer, self-supervised pretraining
- [ ] Ensembling, TTA, pseudo-labeling, final submission

---

## 📋 TRACKED HACKATHONS (Not Currently Active Build)

### 🤖 ARM Create — AI Optimize for Arm-Based Hardware
- **Repository**: https://github.com/oumar-code/arm-ai-optimizer
- **Status**: 📦 Submitted / Tracked
- **Challenge Track**: ARM-powered inference optimization
- **Objective**: Maximize throughput-per-watt on Arm Neoverse architecture
- **Key Metrics**:
  - `avg_latency_ms` ≤ 800 ms
  - `cost_per_run` ≤ $0.05
  - `reliability` ≥ 0.98
  - `quality_score` ≥ 0.85
- **Tech Stack**: Lightweight quantized models (INT8/Q4), batch inference
- **Benchmarks**: Generated under `benchmarks/arm-create_*.json`

---

### 📦 Backblaze GenBlaze — Media Pipeline + B2 Storage
- **Repository**: https://github.com/oumar-code/Aku-Content
- **Path**: `forge/alu-content/` (Backblaze challenge)
- **Status**: 📦 Submitted / Tracked
- **Challenge Track**: AI-powered media processing + zero egress fees
- **Objective**: Demonstrate efficient media metadata extraction at scale using B2
- **Key Angle**: "Zero egress fees, AI metadata at cents per thousand assets"
- **Tech Stack**: AI inference, media processing, Backblaze B2 API
- **Benchmarks**: Generated under `benchmarks/backblaze-genblaze_*.json`

---

### 🌍 African Deep Tech Challenge 2026
- **Repository**: https://github.com/oumar-code/adtc-2026-submission-template
- **Branch**: `main`
- **Status**: 📍 Tracked / Template Active
- **Challenge Scope**: African deep tech innovation ecosystem
- **Key Areas**:
  - EdTech (Akulearn ecosystem)
  - AI/ML for impact
  - Manufacturing & IoT (Coo-Cah Technologies)
- **Submission Template**: Ready for pull requests
- **Integration Points**:
  - Microbiology skills catalogue (AI-powered diagnostics)
  - Global health surveillance with AI
  - Precision medicine applications

---

## ❌ REMOVED / DEPRECATED

### ~~Qwen Cloud Challenge~~ (REMOVED)
- **Reason**: No longer active submission track
- **Previous Path**: `challenges/qwen-cloud/`
- **Status**: Archived / Not pursued
- **Note**: Remove from active challenge rotation

---

## 📊 Hackathon Dashboard

| Challenge | Repo | Status | Key Metric | Deadline | Notes |
|-----------|------|--------|-----------|----------|-------|
| **OpenAI Fashion** 🔴 | oumar-code/oumar-code | 🔨 BUILDING | Demo video ready | July 21 | **PRIMARY FOCUS** |
| **Kaggle — Knee MRI** 🦵 | oumar-code/oumar-code | 🔨 BUILDING | Macro AUC (12 targets) | Rolling | challenges/kaggle-knee-mri/ |
| ARM Create | arm-ai-optimizer | 📦 TRACKED | Cost ≤ $0.05 | Submitted | Arm optimization |
| Backblaze GenBlaze | Aku-Content/forge | 📦 TRACKED | Zero egress | Submitted | Media pipeline |
| African Deep Tech 2026 | adtc-2026-submission-template | 📍 ACTIVE | Ecosystem integration | Rolling | Template active |
| ~~Qwen Cloud~~ | ~~qwen-cloud~~ | ❌ REMOVED | — | — | Archived |

---

## 🎯 Integration Strategy

### Current Build (OpenAI Fashion)
Focus 100% on fashion app — leverage **Microbiology Skills Catalogue** for future EdTech pivots:
- Skill tracker architecture (generalizable to any domain)
- AI tutor agent (adaptable to microbiology Q&A)
- Offline-first infrastructure (essential for African contexts)

### Tracked Submissions
- **ARM Create**: Efficiency-focused infrastructure (ready to reuse)
- **Backblaze GenBlaze**: Media processing + AI (forge/alu-content)
- **African Deep Tech 2026**: Ecosystem narrative (Akulearn + Coo-Cah)

### Future Pivots
- EdTech: Replicate fashion app for microbiology training
- Health: AI diagnostics + disease surveillance (Schistosomiasis research)
- Manufacturing: Coo-Cah integration with predictive AI

---

## 📂 Repository Cross-References

```
oumar-code/
├── oumar-code                      ← OpenAI Fashion 🔴 (ACTIVE BUILD)
│   ├── challenges/openai-fashion/
│   ├── fashion/
│   ├── frontend/
│   └── benchmarks/
│
├── challenges/kaggle-knee-mri     ← Kaggle Knee MRI 🦵 (ACTIVE BUILD)
│   └── README.md
│
├── arm-ai-optimizer                ← ARM Create 📦 (TRACKED)
│   └── benchmarks/arm-create_*.json
│
├── Aku-Content                     ← Backblaze GenBlaze 📦 (TRACKED)
│   └── forge/alu-content/
│       └── backblaze-genblaze_*.json
│
├── adtc-2026-submission-template   ← African Deep Tech 🌍 (ACTIVE)
│   └── submission-template/
│
└── [Other Repos: AkuAI, AkuTutor, Akudemy, Coo-Kah-Doks]
    └── Future hackathon integrations
```

---

## 🚀 Quick Links

### Active Build
- **Main Repo**: https://github.com/oumar-code/oumar-code
- **Submission Checklist**: `challenges/openai-fashion/submission-checklist.md`
- **Demo Script**: `submissions/assets/demo-script-2min.md`
- **Technical Writeup**: `submissions/assets/technical-writeup.md`
- **Kaggle Knee MRI**: `challenges/kaggle-knee-mri/README.md`

### Tracked Hackathons
- **ARM Create**: https://github.com/oumar-code/arm-ai-optimizer
- **Backblaze GenBlaze**: https://github.com/oumar-code/Aku-Content/tree/main/forge/alu-content
- **African Deep Tech 2026**: https://github.com/oumar-code/adtc-2026-submission-template

### Skills & Frameworks
- **Fashion Skills**: `fashion/skill_tracker.py`
- **Microbiology Skills**: `fashion/microbiology_skills.py`
- **Skill Vector DB Export**: `get_vector_representation()` in microbiology_skills.py

---

## 📝 Submission Status Checklist

- [x] **OpenAI Fashion** — Core features complete, awaiting final benchmarks
- [x] **ARM Create** — Benchmarks committed, optimization complete
- [x] **Backblaze GenBlaze** — Media pipeline integrated, cost metrics validated
- [x] **African Deep Tech 2026** — Template active, ready for ecosystem submission
- [x] **Microbiology Skills** — Integrated for future EdTech pivots
- [x] **Hackathon Tracking** — Centralized documentation (this file)
- [ ] **Kaggle — Knee MRI** — Baseline pipeline and multimodal strategy (in progress)

---

**Last Updated**: 2026-09-02  
**Maintainer**: @oumar-code  
**Focus**: OpenAI Fashion 🔨 | Tracking: ARM, Backblaze, African Deep Tech 2026 | Kaggle Knee MRI 🦵
