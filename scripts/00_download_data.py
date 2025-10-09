import os, sys, subprocess, yaml
from src.io_utils import ensure_dir

# Optional: Kaggle download helper (user may also place file manually)
DATA_DEST = 'data/raw/social_media_mental_health.csv'

if os.path.exists(DATA_DEST):
    print('Dataset already present at', DATA_DEST)
    sys.exit(0)

print('Attempting Kaggle download via kaggle CLI...')
print('If this fails, manually place the CSV at data/raw/social_media_mental_health.csv')

# Example (replace with actual Kaggle dataset if needed)
# subprocess.run(['kaggle','datasets','download','-d','<owner>/<dataset>','-p','data/raw','--unzip'], check=False)
