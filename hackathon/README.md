# DSN Bootcamp - How to use TRACKING.md

Purpose
This small README explains how to use the tracking file for your DSN Mart hackathon project.

How to use
1. Copy the `hackathon/` folder into your project root (or clone this branch into a new repo).
2. Add your data files under `data/` (e.g., `data/train.csv`, `data/test.csv`).
3. Update hackathon/TRACKING.md as you progress (check/uncheck tasks, add notes).
4. Create branches for features/experiments (e.g., `feature/lag-features`, `exp/lightgbm-baseline`).
5. Commit reproducible artifacts: notebooks, scripts, and requirements.txt.

Recommended workflow
- Run EDA and write findings to `notebooks/eda.ipynb`.
- Implement features in `src/features.py` and tests in `tests/`.
- Train models in `notebooks/train_baseline.ipynb` and export `models/`.

Copying to a new repo
- In a new repo, create the same `hackathon/` folder and paste TRACKING.md and this README.
- Keep this file updated to show progress to collaborators and mentors.

Good luck — start with milestone 1 (EDA) and update the tracking tasks as you go.