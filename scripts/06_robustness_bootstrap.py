import pandas as pd, numpy as np
import statsmodels.api as sm
from sklearn.ensemble import RandomForestRegressor
from src.io_utils import load_yaml, ensure_dir, write_json, git_commit_or_na, now_iso

params = load_yaml('config/params.yml')
paths = load_yaml('config/paths.yml')

df = pd.read_csv(paths['data_clean'])

y = df['feel_depressed']
X_cols = [c for c in ['interest_fluctuation','comparison_frequency','sleep_issues','distractibility_scale',
                      'avg_time_spent','difficulty_concentrating','seeks_validation'] if c in df.columns]
X = df[X_cols].astype(float)
X_const = sm.add_constant(X)

n = len(df)
B = params['bootstrap']['n_resamples']

betas = []
rf_imps = []

for b in range(B):
    idx = np.random.default_rng(params['seed'] + b).integers(0, n, n)
    Xb, yb = X_const.iloc[idx], y.iloc[idx]
    ols = sm.OLS(yb, Xb, missing='drop').fit()
    betas.append(ols.params.to_dict())

    rf = RandomForestRegressor(
        n_estimators=params['rf']['n_estimators'],
        max_depth=params['rf']['max_depth'],
        max_features=params['rf']['max_features'],
        min_samples_leaf=params['rf']['min_samples_leaf'],
        random_state=params['seed'] + b,
        oob_score=True, bootstrap=True
    ).fit(X.iloc[idx], y.iloc[idx])
    rf_imps.append(dict(zip(X_cols, rf.feature_importances_)))

betas_df = pd.DataFrame(betas)
imps_df = pd.DataFrame(rf_imps)

ensure_dir('outputs/tables')
betas_df.to_csv('outputs/tables/bootstrap_betas.csv', index=False)
imps_df.to_csv('outputs/tables/bootstrap_rf_importances.csv', index=False)

ensure_dir('outputs/metrics')
write_json('outputs/metrics/bootstrap_meta.json', {
  "B": B, "seed": params['seed'], "commit": git_commit_or_na(), "generated_at": now_iso()
})

print('Bootstrap done.')
