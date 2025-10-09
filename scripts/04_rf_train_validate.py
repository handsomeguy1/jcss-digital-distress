import pandas as pd, numpy as np, json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RepeatedKFold, cross_val_score
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
import matplotlib.pyplot as plt
from src.io_utils import load_yaml, ensure_dir, write_json, git_commit_or_na, now_iso

params = load_yaml('config/params.yml')
paths = load_yaml('config/paths.yml')

df = pd.read_csv(paths['data_clean'])

y = df['feel_depressed']
X_cols = [c for c in ['interest_fluctuation','comparison_frequency','sleep_issues','distractibility_scale',
                      'avg_time_spent','difficulty_concentrating','seeks_validation'] if c in df.columns]
X = df[X_cols].astype(float)

rf = RandomForestRegressor(
    n_estimators=params['rf']['n_estimators'],
    max_depth=params['rf']['max_depth'],
    max_features=params['rf']['max_features'],
    min_samples_leaf=params['rf']['min_samples_leaf'],
    random_state=params['seed'],
    oob_score=True,
    bootstrap=True
)

rkf = RepeatedKFold(n_splits=params['cv']['folds'], n_repeats=params['cv']['repeats'], random_state=params['seed'])
cv_r2 = cross_val_score(rf, X, y, scoring='r2', cv=rkf).mean()

rf.fit(X, y)
oob = getattr(rf, 'oob_score_', None)

ensure_dir('outputs/metrics')
write_json('outputs/metrics/rf_cv.json', {
  "cv_R2": float(cv_r2),
  "oob": float(oob) if oob is not None else None,
  "features": X_cols,
  "commit": git_commit_or_na(),
  "generated_at": now_iso()
})

# Permutation importance
imp = permutation_importance(rf, X, y, n_repeats=10, random_state=params['seed'])
imp_tbl = pd.DataFrame({'feature': X_cols, 'importance_mean': imp.importances_mean, 'importance_std': imp.importances_std})
ensure_dir('outputs/tables')
imp_tbl.sort_values('importance_mean', ascending=False).to_csv('outputs/tables/rf_permutation_importance.csv', index=False)

# PDPs for top 3
top3 = imp_tbl.sort_values('importance_mean', ascending=False)['feature'].head(3).tolist()
ensure_dir('outputs/figures')
for ftr in top3:
    fig = plt.figure()
    PartialDependenceDisplay.from_estimator(rf, X, [ftr])
    plt.tight_layout()
    fig.savefig(f"outputs/figures/pdp_{ftr}.png", dpi=300)
    plt.close(fig)

print('RF done. CV-R2=', cv_r2, 'OOB=', oob)
