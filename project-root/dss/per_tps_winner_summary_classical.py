"""
per_tps_winner_summary.py
Summarizes how many times each algorithm wins per TPS level
based on DSS outputs from all priority combinations.
"""

import os
import pandas as pd
import re
from collections import defaultdict

# === 1. Paths ===
batch_dir = "results/fuzzy_batch"
summary_file = os.path.join(batch_dir, "summary_recommendations.csv")
output_file = os.path.join(batch_dir, "per_tps_winner_summary.csv")

if not os.path.exists(summary_file):
    raise FileNotFoundError(f"❌ DSS summary file not found at {summary_file}")

# === 2. Initialize counter: {tps_level: {algorithm: count}} ===
tps_wins = defaultdict(lambda: defaultdict(int))

# === 3. Process each DSS score file ===
for file in os.listdir(batch_dir):
    if not file.startswith("scores_") or not file.endswith(".csv"):
        continue

    df = pd.read_csv(os.path.join(batch_dir, file))

    # Extract TPS level from each scenario
    def get_tps_level(s):
        match = re.search(r"_(\d+)tps", s)
        return f"{match.group(1)}tps" if match else None

    df["tps_level"] = df["scenario"].apply(get_tps_level)

    # Winner algorithm per TPS level
    for tps in df["tps_level"].dropna().unique():
        sub_df = df[df["tps_level"] == tps]
        winner_row = sub_df.loc[sub_df["suitability_score"].idxmax()]
        winner_algo = winner_row["algorithm"]
        tps_wins[tps][winner_algo] += 1

# === 4. Format output ===
records = []
for tps_level in sorted(tps_wins):
    for algo, count in sorted(tps_wins[tps_level].items(), key=lambda x: x[1], reverse=True):
        records.append({
            "tps_level": tps_level,
            "algorithm": algo,
            "scenario_win_count": count
        })

# === 5. Save summary ===
result_df = pd.DataFrame(records)
result_df.to_csv(output_file, index=False)

print(f"\n✅ TPS-level algorithm win summary saved to:\n  {output_file}")
