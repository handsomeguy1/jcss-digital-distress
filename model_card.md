# Model Card — Digital Distress Models

**Intended use.** Research on behavioral correlates of depressive affect; not for clinical or individual diagnosis.

**Data.** Public survey on social media and mental health (Kaggle). Ages ~15–45 after filtering.

**Models.**
- OLS regression for interpretable baselines.
- Random Forest for nonlinear patterns and permutation importance.

**Validation.** Repeated CV, OOB, bootstrap CIs, subgroup error.

**Ethics & limits.**
- Self-reported measures; potential biases.
- Not for individual risk scoring.
- Use results in aggregate and with caution.
