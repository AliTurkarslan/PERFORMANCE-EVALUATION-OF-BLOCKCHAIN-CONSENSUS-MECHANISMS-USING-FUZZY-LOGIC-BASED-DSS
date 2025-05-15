"""
Correctly summarizes the true winner per TPS level by extracting base TPS from each scenario.
Avoids treating poa_100tps, pos_100tps as separate groups.
"""

import os
import pandas as pd
import re
from collections import defaultdict

# === 1. Paths ===
batch_dir = "results/fuzzy_batch"
summary_file = os.path.join(batch_dir, "summary_recommendations.csv")

if not os.path.exists(summary_file):
    raise FileNotFoundError(f"❌ Summary file not found: {summary_file}")

# === 2. Initialize TPS-level win counter ===
tps_wins = defaultdict(lambda: defaultdict(int))  # {tps_level: {algorithm: count}}

# === 3. Go through each scores file ===
for file in os.listdir(batch_dir):
    if not file.startswith("scores_") or not file.endswith(".csv"):
        continue

    file_path = os.path.join(batch_dir, file)
    df = pd.read_csv(file_path)

    # Extract base TPS level from each row's scenario
    def extract_tps(s):
        match = re.search(r'_(\d+)tps', s)
        return f"{match.group(1)}tps" if match else "unknown"

    df["tps_level"] = df["scenario"].apply(extract_tps)

    # For each TPS level (50, 100, 500), find best scoring algorithm
    for tps in df["tps_level"].unique():
        sub = df[df["tps_level"] == tps]
        if sub.empty:
            continue

        winner_row = sub.loc[sub["suitability_score"].idxmax()]
        winning_alg = winner_row["algorithm"]
        tps_wins[tps][winning_alg] += 1

# === 4. Format results ===
records = []
for tps_level, algos in sorted(tps_wins.items()):
    for algorithm, count in sorted(algos.items(), key=lambda x: x[1], reverse=True):
        records.append({
            "tps_level": tps_level,
            "algorithm": algorithm,
            "scenario_win_count": count
        })

result_df = pd.DataFrame(records)
out_path = os.path.join(batch_dir, "per_tps_winner_summary.csv")
result_df.to_csv(out_path, index=False)

print(f"\n✅ Corrected TPS-level algorithm wins saved to:\n  {out_path}")
