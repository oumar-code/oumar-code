# DSN Bootcamp - Project Tracking

Objective: Build a predictive model for DSN Mart to forecast total product-store sales for the DSN AI Bootcamp qualification hackathon.

Dataset: Place training and test CSVs in the project `data/` directory (e.g., `data/train.csv`, `data/test.csv`).

Milestones:
- 0. Setup (this tracking file)
- 1. Data exploration & cleaning
- 2. Feature engineering (date, lag, rolling, store/product aggregates)
- 3. Baseline model (LightGBM) with time-aware CV
- 4. Model improvements (target encoding, tuning, ensembles)
- 5. Final training & submission

Kanban-style tasks (update status as you progress):
- [ ] Data ingest & schema check
- [ ] EDA report
- [ ] Feature engineering scripts
- [ ] Baseline notebook
- [ ] CV & OOF scoring
- [ ] Hyperparameter tuning
- [ ] Final submission

Notes:
- Evaluation metric: RMSE (use root_mean_squared_error on raw target)
- Use time-based CV to avoid leakage (train dates must predate validation dates)
- Keep experiments reproducible: record random seeds, package versions, and notebook outputs

Next steps:
- Create project repo and copy these files into the new repo's root or `hackathon/` directory.
- Populate `data/` with train/test files and begin milestone 1.