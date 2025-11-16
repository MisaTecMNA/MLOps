"""
Script to generate a drifted version of insurance_clean.csv for drift detection demo.
"""
import pandas as pd
import numpy as np
import random

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# Load clean data
clean_path = "c:/Users/mizlop/OneDrive - SAS/Documents/SAS_git/MLOps/FaseFinal_team42/data/processed/insurance_clean.csv"
df = pd.read_csv(clean_path)

# Simulate drift:
# 1. Shift mean of 'DemAvgIncome' by +20%
if 'DemAvgIncome' in df.columns:
    df['DemAvgIncome'] = df['DemAvgIncome'] * 1.2
# 2. Add noise to 'AvgAge' (simulate aging population)
if 'AvgAge' in df.columns:
    df['AvgAge'] = df['AvgAge'] + np.random.normal(2, 1, size=len(df))
# 3. Change distribution of 'DemNoReligion' (simulate secularization)
if 'DemNoReligion' in df.columns:
    df['DemNoReligion'] = df['DemNoReligion'] + np.random.binomial(1, 0.2, size=len(df))
# 4. Flip 10% of target 'MoHoPol' (simulate label noise)
if 'MoHoPol' in df.columns:
    flip_idx = np.random.choice(df.index, size=int(0.1*len(df)), replace=False)
    df.loc[flip_idx, 'MoHoPol'] = 1 - df.loc[flip_idx, 'MoHoPol']

# Save drifted data
out_path = "c:/Users/mizlop/OneDrive - SAS/Documents/SAS_git/MLOps/FaseFinal_team42/data/processed/insurance_drift.csv"
df.to_csv(out_path, index=False)
print(f"Drifted data saved to {out_path}")
