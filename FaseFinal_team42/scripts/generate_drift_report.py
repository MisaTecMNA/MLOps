"""
Script to compare metrics and distributions between clean and drifted datasets, and save plots/reports for drift analysis.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

REPORT_DIR = r"C:/Users/mizlop/OneDrive - SAS/Documents/SAS_git/MLOps/FaseFinal_team42/reports/data_drift"
os.makedirs(REPORT_DIR, exist_ok=True)

CLEAN_PATH = r"C:/Users/mizlop/OneDrive - SAS/Documents/SAS_git/MLOps/FaseFinal_team42/data/processed/insurance_clean.csv"
DRIFT_PATH = r"C:/Users/mizlop/OneDrive - SAS/Documents/SAS_git/MLOps/FaseFinal_team42/data/processed/insurance_drift.csv"

# Load data
df_clean = pd.read_csv(CLEAN_PATH)
df_drift = pd.read_csv(DRIFT_PATH)

# Columns to compare
target = 'MoHoPol'
num_cols = ['DemAvgIncome', 'AvgAge']
cat_cols = ['DemNoReligion']

# 1. Plot distributions for selected columns
for col in num_cols + cat_cols:
    plt.figure(figsize=(8,4))
    plt.hist(df_clean[col], bins=30, alpha=0.5, label='Clean', color='blue', density=True)
    plt.hist(df_drift[col], bins=30, alpha=0.5, label='Drifted', color='red', density=True)
    plt.title(f"Distribution of {col}: Clean vs Drifted")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, f"dist_{col}.png"))
    plt.close()

# 2. Compare target distribution
plt.figure(figsize=(6,4))
plt.hist(df_clean[target], bins=2, alpha=0.5, label='Clean', color='blue', density=True)
plt.hist(df_drift[target], bins=2, alpha=0.5, label='Drifted', color='red', density=True)
plt.title(f"Target ({target}) Distribution: Clean vs Drifted")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, f"dist_{target}.png"))
plt.close()

# 3. Compute and save summary statistics
def get_metrics(df):
    return {
        'DemAvgIncome_mean': float(np.mean(df['DemAvgIncome'])),
        'DemAvgIncome_std': float(np.std(df['DemAvgIncome'])),
        'AvgAge_mean': float(np.mean(df['AvgAge'])),
        'AvgAge_std': float(np.std(df['AvgAge'])),
        'DemNoReligion_mean': float(np.mean(df['DemNoReligion'])),
        'MoHoPol_mean': float(np.mean(df['MoHoPol'])),
        'MoHoPol_std': float(np.std(df['MoHoPol'])),
    }

metrics_clean = get_metrics(df_clean)
metrics_drift = get_metrics(df_drift)

with open(os.path.join(REPORT_DIR, "metrics_clean.json"), "w") as f:
    json.dump(metrics_clean, f, indent=2)
with open(os.path.join(REPORT_DIR, "metrics_drift.json"), "w") as f:
    json.dump(metrics_drift, f, indent=2)

# 4. Save a summary report
with open(os.path.join(REPORT_DIR, "drift_report.txt"), "w") as f:
    f.write("Data Drift Report\n=================\n")
    f.write("\n--- Clean Data Metrics ---\n")
    f.write(json.dumps(metrics_clean, indent=2))
    f.write("\n--- Drifted Data Metrics ---\n")
    f.write(json.dumps(metrics_drift, indent=2))
    f.write("\n\nSee PNG files for distribution plots.\n")

print(f"Drift analysis report and plots saved in {REPORT_DIR}")
