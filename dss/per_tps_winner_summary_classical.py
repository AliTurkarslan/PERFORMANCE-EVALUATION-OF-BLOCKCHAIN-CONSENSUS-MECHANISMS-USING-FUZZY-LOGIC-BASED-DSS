"""
per_tps_winner_summary_classical.py
Summarizes how many times each algorithm wins per TPS level
based on classical weighted scores from all priority combinations.
"""

import os
import pandas as pd
import re
from collections import defaultdict

# === 1. Paths ===
batch_dir = "results/classical_batch"
output_file = os.path.join(batch_dir, "per_tps_winner_summary.csv")

if not os.path.exists(batch_dir):
    raise FileNotFoundError(f"❌ Directory not found: {batch_dir}")

# === 2. Initialize counter: {tps_level: {algorithm: count}} ===
tps_wins = defaultdict(lambda: defaultdict(int))

# === 3. Process each classical score file ===
for file in os.listdir(batch_dir):
    if not file.startswith("scores_") or not file.endswith(".csv"):
        continue

    df = pd.read_csv(os.path.join(batch_dir, file))

    def get_tps_level(s):
        match = re.search(r"_(\d+)tps", s)
        return f"{match.group(1)}tps" if match else None

    df["tps_level"] = df["scenario"].apply(get_tps_level)

    for tps in df["tps_level"].dropna().unique():
        sub_df = df[df["tps_level"] == tps]
        winner_row = sub_df.loc[sub_df["classical_score"].idxmax()]
        winner_algo = winner_row["algorithm"]
        tps_wins[tps][winner_algo] += 1

# === 4. Format and save ===
records = []
for tps_level in sorted(tps_wins):
    for algo, count in sorted(tps_wins[tps_level].items(), key=lambda x: x[1], reverse=True):
        records.append({
            "tps_level": tps_level,
            "algorithm": algo,
            "scenario_win_count": count
        })

result_df = pd.DataFrame(records)
result_df.to_csv(output_file, index=False)

print(f"\n✅ Classical TPS-level win summary saved to:\n  {output_file}")
