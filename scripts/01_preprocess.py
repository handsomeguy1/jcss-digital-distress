import pandas as pd
import yaml
from src.io_utils import load_yaml, ensure_dir

paths = load_yaml('config/paths.yml')

df = pd.read_csv(paths['data_raw'])

# Minimalist cleaning example — adapt to actual headers
keep_cols = [
    'feel_depressed','comparison_frequency','seeks_validation','distractibility_scale',
    'difficulty_concentrating','interest_fluctuation','sleep_issues','avg_time_spent',
    'usage_without_purpose','distraction_while_busy','age','gender','relationship_status','occupation_status'
]
df = df[[c for c in keep_cols if c in df.columns]].copy()

# Basic sanity filters (example)
df = df[(df['age']>=15) & (df['age']<=45)] if 'age' in df.columns else df

ensure_dir('outputs/derived')
df.to_csv(paths['data_clean'], index=False)
print('Wrote', paths['data_clean'], df.shape)
