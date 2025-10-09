# JCSS Digital Distress — Reproducible Pipeline
Digital Distress in the Attention Economy: A Dual-Model Analysis
Shakir, S. (2025).
This repository reproduces the analyses for the paper *Modeling the Behavioral Dynamics of Digital Distress*.

## Overview
This repository contains all materials required to reproduce the analyses reported in
“Digital Distress in the Attention Economy: A Dual-Model Analysis.”
The study integrates Ordinary Least Squares (OLS) regression and a Random Forest model to examine how social comparison, validation-seeking, attentional fluctuation, and sleep disruption predict depressive affect.
It operationalizes a methodologically pluralist pipeline—combining interpretive transparency with nonlinear discovery.

## Environment Setup
1. Clone the repository
   git clone https://github.com/handsomeguy1/jcss-digital-distress.git
cd jcss-digital-distress

2. Create the conda environment
   conda env create -f environment.yml
conda activate jcss-distress

3. Run the full pipeline
python scripts/01_preprocess.py
python scripts/03_ols_baseline.py
python scripts/04_rf_train_validate.py
python scripts/05_importance_pdp.py
python scripts/06_robustness_bootstrap.py
python scripts/07_subgroup_errors.py


## Pipeline Description
| Step | Script                       | Purpose                                                         | Output                                                                |
| ---- | ---------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------- |
| 1    | `01_preprocess.py`           | Minimalist data cleaning and auditing                           | `data/cleaned_social_media.csv`                                       |
| 2    | `03_ols_baseline.py`         | OLS regression, diagnostics, VIF, coefficient table             | `outputs/ols_coefficients.csv`, `outputs/vif.csv`                     |
| 3    | `04_rf_train_validate.py`    | Random Forest with cross-validation and OOB scoring             | `outputs/rf_metrics.csv`                                              |
| 4    | `05_importance_pdp.py`       | Permutation importance + Partial Dependence Plots               | `outputs/pdp_*.png`                                                   |
| 5    | `06_robustness_bootstrap.py` | Bootstrap confidence intervals for coefficients and importances | `outputs/bootstrap_betas.csv`, `outputs/bootstrap_rf_importances.csv` |
| 6    | `07_subgroup_errors.py`      | MAE/RMSE error analysis by gender and relationship status       | `outputs/subgroup_errors.csv`                                         |


Key Results (Replicable)
| Metric              | Value                                                 |
| ------------------- | ----------------------------------------------------- |
| OLS Adjusted R²     | **0.35**                                              |
| Random Forest CV-R² | **0.30**                                              |
| Random Forest OOB   | **0.31**                                              |
| Bootstrap Resamples | **300**                                               |
| Primary Predictors  | Interest fluctuation, social comparison, sleep issues |

## Interpretation
The OLS model identifies key linear predictors of depressive affect; the Random Forest validates these relationships while uncovering nonlinear thresholds. Together, they reveal that digital distress arises from convergent behavioural loops—attention fragmentation, social comparison, and sleep disruption—rather than single-factor exposure effects.

## Reproducibility & Citation
@software{shakir2025digitaldistress,
  author    = {Shakir, S.},
  title     = {Digital Distress in the Attention Economy: A Dual-Model Analysis},
  year      = {2025},
  publisher = {Zenodo},
  version   = {1.0},
  doi       = {10.xxxx/zenodo.xxxxxx}
}

Code: MIT. Data: follow the Kaggle dataset license.
Cite using `CITATION.cff`.
