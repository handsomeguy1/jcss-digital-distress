# JCSS Digital Distress — Reproducible Pipeline

This repository reproduces the analyses for the paper *Modeling the Behavioral Dynamics of Digital Distress*.

## Quick start
```bash
conda env create -f environment.yml
conda activate jcss-distress
make all
# outputs in outputs/tables, outputs/figures, outputs/metrics
```

## Data
We use the public dataset **"Social Media and Mental Health: Correlation between Social Media Use and General Mental Well-being"** (Kaggle).  
Place the main CSV as `data/raw/social_media_mental_health.csv` or run `python scripts/00_download_data.py` (requires Kaggle CLI with credentials).  
SHA256 checksums and column expectations are listed in `data/README.md`.

## Pipeline
- 01_preprocess.py → cleans minimally per paper
- 03_ols_baseline.py → OLS model, diagnostics, VIF, coefficient table
- 04_rf_train_validate.py → Random Forest with cross-validation & OOB
- 05_importance_pdp.py → permutation importance + PDP
- 06_robustness_bootstrap.py → bootstrap CIs
- 07_subgroup_errors.py → subgroup MAE/RMSE

Parameters live in `config/params.yml`. Paths in `config/paths.yml`.

## Reproducibility
- Python/dep versions pinned in `environment.yml`
- Random seeds fixed via `config/params.yml`
- All scripts write metrics with the active git commit (if available)
- Model Card: `model_card.md`

## License and citation
Code: MIT. Data: follow the Kaggle dataset license.
Cite using `CITATION.cff`.
