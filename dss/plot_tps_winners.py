"""
plot_tps_winners.py
Visualizes the number of scenario wins per algorithm across TPS levels.
Generates both a stacked bar chart and a heatmap.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. Load data ===
input_path = "results/fuzzy_batch/per_tps_winner_summary.csv"
if not os.path.exists(input_path):
    raise FileNotFoundError(f"❌ File not found: {input_path}")

df = pd.read_csv(input_path)

# === 2. Prepare pivot table: rows = TPS, columns = algorithms ===
tps_order = ["50tps", "100tps", "500tps"]
algo_order = ["POA", "POS", "POW"]

pivot_df = df.pivot(index="tps_level", columns="algorithm", values="scenario_win_count").fillna(0)

# Ensure expected order
for algo in algo_order:
    if algo not in pivot_df.columns:
        pivot_df[algo] = 0
pivot_df = pivot_df[algo_order]
pivot_df = pivot_df.reindex(tps_order)

# === 3. Plot: Stacked bar chart ===
plt.figure(figsize=(10, 6))
pivot_df.plot(kind="bar", stacked=True, colormap="tab20", edgecolor="black")
plt.title("Scenario Wins per Algorithm by TPS Level")
plt.xlabel("TPS Level")
plt.ylabel("Scenario Win Count")
plt.xticks(rotation=0)
plt.legend(title="Algorithm", loc="upper right")
plt.tight_layout()
bar_path = "results/fuzzy_batch/stacked_bar_tps_wins.png"
plt.savefig(bar_path, dpi=300)
plt.close()
print(f"📊 Stacked bar chart saved to:\n  {bar_path}")

# === 4. Plot: Heatmap ===
plt.figure(figsize=(6, 4))
sns.heatmap(pivot_df, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, cbar=True)
plt.title("Heatmap of Algorithm Scenario Wins by TPS")
plt.xlabel("Algorithm")
plt.ylabel("TPS Level")
plt.tight_layout()
heatmap_path = "results/fuzzy_batch/heatmap_tps_wins.png"
plt.savefig(heatmap_path, dpi=300)
plt.close()
print(f"🔥 Heatmap saved to:\n  {heatmap_path}")
