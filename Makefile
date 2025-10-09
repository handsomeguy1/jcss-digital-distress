.PHONY: all data prep ols rf interpret robust subgroup figs

all: data prep ols rf interpret robust subgroup figs

data:
	python scripts/00_download_data.py

prep:
	python scripts/01_preprocess.py

ols:
	python scripts/03_ols_baseline.py

rf:
	python scripts/04_rf_train_validate.py

interpret:
	python scripts/05_importance_pdp.py

robust:
	python scripts/06_robustness_bootstrap.py

subgroup:
	python scripts/07_subgroup_errors.py

figs:
	python scripts/99_render_figures.py
