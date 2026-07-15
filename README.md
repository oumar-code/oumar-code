<!-- Hackathon Backbone -->
## 🏗️ Hackathon Backbone — Quickstart

> **Build once, adapt fast.** One shared pipeline. Three challenge overlays. Five-command first run.

```bash
# 1. Clone & enter
git clone https://github.com/oumar-code/oumar-code && cd oumar-code

# 2. Bootstrap environment
python3 scripts/setup.py          # copies .env.example → .env, installs deps

# 3. Edit .env — add MODEL_ENDPOINT + MODEL_API_KEY (or skip for stub mode)

# 4. Run a challenge (safe profile — recommended for demos)
make run CHALLENGE=arm-create PROFILE=safe

# 5. Evaluate & generate benchmark artifacts
make eval CHALLENGE=arm-create PROFILE=safe

# 6. Switch challenge in 5 minutes
make eval CHALLENGE=backblaze-genblaze PROFILE=safe

# 7. Full benchmark sweep (all challenges × profiles)
make benchmark

# 8. Launch interactive demo
make demo

# 9. View benchmark report
cat benchmarks/report.md

# 10. Check submission checklist
cat challenges/arm-create/submission-checklist.md
```

### Repository Layout

```
core/               Shared pipeline (ingestion, serving, evaluation, UI)
scripts/            run.py · setup.py · benchmark.py
config/             safe.env · aggressive.env (base profiles)
challenges/         arm-create/ · backblaze-genblaze/ · qwen-cloud/
benchmarks/         Committed baseline + auto-generated run artifacts
submissions/        Judging assets, templates, runbook
Makefile            All commands above
.env.example        Copy to .env, fill in API keys
```

### How to Switch Challenges in Under 5 Minutes
1. Pick: `arm-create` | `backblaze-genblaze` | `qwen-cloud`
2. Read KPIs: `challenges/<name>/kpi.md`
3. Check config: `challenges/<name>/config.safe.env`
4. Run: `make eval CHALLENGE=<name> PROFILE=safe`
5. Artifacts land in `benchmarks/` automatically.

---

<!-- Header -->
<h1 align="center">Hey, I'm Oumar 👋</h1>
<h3 align="center">Full-Stack Engineer · EdTech Builder · AI & Offline-First Systems</h3>

<p align="center">
  <a href="https://github.com/oumar-code/AkuAI">
    <img src="https://img.shields.io/badge/🎓%20Akulearn-Active-brightgreen?style=for-the-badge" />
  </a>
  <a href="https://github.com/oumar-code/Coo-Kah-Doks">
    <img src="https://img.shields.io/badge/🏭%20Coo--Cah%20Technologies-Active-brightgreen?style=for-the-badge" />
  </a>
  <img src="https://img.shields.io/badge/Focus-Africa%20EdTech%20%2B%20AI-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Building-blue?style=for-the-badge" />
</p>

---

## 👨‍💻 About Me

I'm a full-stack engineer and founder building AI-powered, offline-first systems for underserved communities across Africa. My background spans Python/FastAPI backends, Next.js frontends, Kotlin Multiplatform mobile, and edge AI/ML deployment.

Currently I'm heads-down on **Akulearn** — an EdTech ecosystem that delivers AI-powered education where internet infrastructure is unreliable, combining LLM inference, offline IoT edge hardware, blockchain credentials, eSIM provisioning, and solar-powered delivery. Alongside that, I'm architecting **Coo-Cah Technologies**, a vertically-integrated AI-powered smart manufacturing group across Nigeria, Rwanda, and Kenya.

**Tech I work with:**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=flat&logo=kotlin&logoColor=white" />
  <img src="https://img.shields.io/badge/Kotlin%20Multiplatform-7F52FF?style=flat&logo=kotlin&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/AI%2FML-FF6F00?style=flat&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/IoT%20%2F%20Edge-00BCD4?style=flat&logo=raspberrypi&logoColor=white" />
  <img src="https://img.shields.io/badge/Blockchain-121D33?style=flat&logo=ethereum&logoColor=white" />
</p>

---

## 🚀 What I'm Building Now

- 🔭 **Akulearn** — AI + offline-first EdTech platform for Nigeria and broader Africa
- 🏭 **Coo-Cah Technologies** — Pan-African AI-powered smart manufacturing ecosystem
- 🌱 Exploring: Kotlin Multiplatform, LLM fine-tuning (Phi-3.5, Gemma), edge inference
- 🤝 Open to: EdTech, AI/ML, impact-driven engineering roles, and strategic partnerships

---

## 🎓 Akulearn Ecosystem

> **Akulearn** is genuinely differentiated — it combines AI inference, blockchain credentials, offline IoT edge hardware, eSIM provisioning, and solar power to deliver quality education to underserved African communities. This isn't a CRUD app; it's a full platform.

| Project | What it does | Stack |
|---------|-------------|-------|
| <a href="https://github.com/oumar-code/AkuAI">AkuAI</a> | AI inference layer — text generation, Gemma LLM serving | Python, FastAPI |
| <a href="https://github.com/oumar-code/AkuTutor">AkuTutor</a> | AI-powered tutor with curriculum Q&A and adaptive learning | Python, FastAPI |
| <a href="https://github.com/oumar-code/Aku-EdgeHub">Aku-EdgeHub</a> | Offline edge server for underserved / low-connectivity areas | Python, IoT |
| <a href="https://github.com/oumar-code/Akudemy">Akudemy</a> | Academy platform — course delivery and learner management | Next.js, FastAPI |
| <a href="https://github.com/oumar-code/AkuWorkspace">AkuWorkspace</a> | Collaborative workspace for learners and educators | Next.js, Python |

📖 Full documentation: [oumar-code.github.io/Akulearn_docs](https://oumar-code.github.io/Akulearn_docs/)

---

## 🏭 Coo-Cah Technologies

> A vertically-integrated, AI-orchestrated smart manufacturing group — Africa's own industrial operating system.

| What | Detail |
|------|--------|
| **Scope** | Multi-country manufacturing group (NG · RW · KE) |
| **Verticals** | Electronics · Chemicals · Consumer Goods · Lifestyle |
| **Technology Core** | AI Platform · MES · Digital Twins · AMR Fleets · Cobots |
| **Energy** | Solar + Wind + Hybrid — targeting 90% energy self-sufficiency |
| **Flagship** | Project Baobab — Africa's first indigenous semiconductor lab |

<a href="https://github.com/oumar-code/Coo-Kah-Doks">📂 See the Coo-Cah Blueprint →</a>

---

## 🏆 Milestones & Recognition

- 🎯 **iDICE Founders Lab — Cohort 1** participant (registered with Aku)
- 🚀 **Acelerate Africa** — Applied with Coo-Cah Technologies as COO
- 📊 Acelerate Africa Assessment Score: **81 / 100**

---

## 📊 GitHub Stats

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=oumar-code&show_icons=true&theme=dark&hide_border=true" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=oumar-code&layout=compact&theme=dark&hide_border=true" />
</p>

---

## 📬 Let's Connect

Building something ambitious in African EdTech, AI, or manufacturing? Let's talk.

<p align="center">
  <a href="https://oumar-code.github.io/Akulearn_docs/">📖 Akulearn Docs</a> ·
  <a href="https://github.com/oumar-code/Coo-Kah-Doks">📂 Coo-Cah Blueprint</a> ·
  <a href="mailto:umarabubakarg2018@gmail.com">✉️ Email Me</a>
</p>

---

<p align="center"><i>"The most powerful force in the African economy is the African who decides to build it."</i></p>

