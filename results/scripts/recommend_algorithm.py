"""
Step 3 - Recommend the best consensus algorithm
Reads the DSS suitability scores and identifies the top-performing algorithm.
"""

import pandas as pd
import os

# Load DSS output
input_file = "results/fuzzy_dss/dss_suitability_scores.csv"

if not os.path.exists(input_file):
    raise FileNotFoundError(f"File not found: {input_file}")

df = pd.read_csv(input_file)

# Drop any rows with missing scores (optional safety step)
df = df.dropna(subset=["suitability_score"])

# Group by algorithm and calculate average score
summary = (
    df.groupby("algorithm")["suitability_score"]
    .mean()
    .reset_index()
    .sort_values(by="suitability_score", ascending=False)
)

# Display summary
print("\n📊 Average DSS Suitability Score per Algorithm:")
print(summary.to_string(index=False, float_format="%.3f"))

# Top recommendation
best = summary.iloc[0]
print(f"\n✅ Recommended Algorithm: {best['algorithm']} "
      f"(Average Suitability Score: {best['suitability_score']:.3f})")
