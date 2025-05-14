"""
Visualize TPS-level algorithm winner counts using bar chart and heatmap.
Input: per_tps_winner_summary.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === 1. Load Data ===
file_path = "results/fuzzy_batch/per_tps_winner_summary.csv"
df = pd.read_csv(file_path)

# Ensure order
tps_order = ["50tps", "100tps", "500tps"]
algo_order = ["POA", "POS", "POW"]

# === 2. Pivot for plotting ===
pivot_df = df.pivot(index="tps_level", columns="algorithm", values="scenario_win_count").fillna(0)

# Ensure all 3 algorithms exist as columns (even if 0)
for alg in algo_order:
    if alg not in pivot_df.columns:
        pivot_df[alg] = 0

# Reorder rows and columns
pivot_df = pivot_df[algo_order]
pivot_df = pivot_df.reindex(tps_order)

# === 3. Plot - Stacked Bar ===
plt.figure(figsize=(10, 6))
pivot_df.plot(kind="bar", stacked=True, colormap="tab20", edgecolor="black")
plt.title("Scenario Wins per Algorithm by TPS Level")
plt.ylabel("Scenario Win Count")
plt.xlabel("TPS Level")
plt.xticks(rotation=0)
plt.legend(title="Algorithm", loc="upper right")
plt.tight_layout()
plt.savefig("results/fuzzy_batch/stacked_bar_tps_wins.png", dpi=300)
plt.close()
print("📊 Stacked bar chart saved: results/fuzzy_batch/stacked_bar_tps_wins.png")

# === 4. Plot - Heatmap ===
plt.figure(figsize=(6, 4))
sns.heatmap(pivot_df, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, cbar=True)
plt.title("Heatmap of Algorithm Wins per TPS Level")
plt.ylabel("TPS Level")
plt.xlabel("Algorithm")
plt.tight_layout()
plt.savefig("results/fuzzy_batch/heatmap_tps_wins.png", dpi=300)
plt.close()
print("🔥 Heatmap saved: results/fuzzy_batch/heatmap_tps_wins.png")
