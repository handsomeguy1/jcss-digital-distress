import pandas as pd, numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor
from src.io_utils import load_yaml, ensure_dir

params = load_yaml('config/params.yml')
paths = load_yaml('config/paths.yml')

df = pd.read_csv(paths['data_clean'])

y = df['feel_depressed']
X_cols = [c for c in ['interest_fluctuation','comparison_frequency','sleep_issues','distractibility_scale',
                      'avg_time_spent','difficulty_concentrating','seeks_validation'] if c in df.columns]
X = df[X_cols].astype(float)

rkf = RepeatedKFold(n_splits=params['cv']['folds'], n_repeats=params['cv']['repeats'], random_state=params['seed'])

def cv_mae_mask(mask):
    maes = []
    for train, test in rkf.split(X[mask]):
        tr, te = X[mask].iloc[train], X[mask].iloc[test]
        yr, ye = y[mask].iloc[train], y[mask].iloc[test]
        rf = RandomForestRegressor(
            n_estimators=params['rf']['n_estimators'],
            max_depth=params['rf']['max_depth'],
            max_features=params['rf']['max_features'],
            min_samples_leaf=params['rf']['min_samples_leaf'],
            random_state=params['seed'],
            oob_score=False, bootstrap=True
        )
        rf.fit(tr, yr)
        pred = rf.predict(te)
        maes.append(mean_absolute_error(ye, pred))
    return float(np.mean(maes))

groups = {}
if 'gender' in df.columns:
    for g in df['gender'].dropna().unique():
        mask = df['gender'] == g
        groups[f'gender={g}'] = cv_mae_mask(mask)

if 'relationship_status' in df.columns:
    for g in df['relationship_status'].dropna().unique():
        mask = df['relationship_status'] == g
        groups[f'rel={g}'] = cv_mae_mask(mask)

ensure_dir('outputs/tables')
pd.DataFrame([{"group":k,"cv_mae":v} for k,v in groups.items()]).to_csv('outputs/tables/subgroup_mae.csv', index=False)
print('Subgroup MAE saved.')
