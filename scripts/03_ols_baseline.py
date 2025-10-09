import pandas as pd, numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from src.io_utils import load_yaml, ensure_dir, write_json, git_commit_or_na, now_iso

paths = load_yaml('config/paths.yml')

df = pd.read_csv(paths['data_clean'])

y = df['feel_depressed']
X_cols = [c for c in ['interest_fluctuation','comparison_frequency','sleep_issues','distractibility_scale',
                      'avg_time_spent','difficulty_concentrating','seeks_validation'] if c in df.columns]
X = df[X_cols].astype(float)
X = sm.add_constant(X)

model = sm.OLS(y, X, missing='drop').fit()

# VIF
vif = []
X_no_const = X.drop(columns=['const'])
for i, col in enumerate(X_no_const.columns):
    vif.append({'variable': col, 'vif': variance_inflation_factor(X_no_const.values, i)})
vif_df = pd.DataFrame(vif)
ensure_dir('outputs/tables')
vif_df.to_csv('outputs/tables/vif.csv', index=False)

coefs = model.summary2().tables[1]
coefs.to_csv('outputs/tables/ols_coefficients.csv')

metrics = {
  "r2_adj": float(model.rsquared_adj),
  "n": int(model.nobs),
  "commit": git_commit_or_na(),
  "generated_at": now_iso()
}
ensure_dir('outputs/metrics')
write_json('outputs/metrics/ols_metrics.json', metrics)

print('OLS done. Adj R2=', metrics['r2_adj'])
