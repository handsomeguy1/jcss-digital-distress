import numpy as np
from sklearn.model_selection import RepeatedKFold, cross_val_score

def repeated_cv(estimator, X, y, scoring, n_splits, n_repeats, random_state):
    rkf = RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)
    scores = cross_val_score(estimator, X, y, scoring=scoring, cv=rkf, n_jobs=None)
    return float(np.mean(scores)), float(np.std(scores))
