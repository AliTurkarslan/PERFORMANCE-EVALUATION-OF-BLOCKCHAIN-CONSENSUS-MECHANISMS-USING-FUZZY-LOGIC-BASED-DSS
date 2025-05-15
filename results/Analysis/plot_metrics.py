import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load metrics data
df = pd.read_csv("results/all_metrics.csv")
df["algorithm"] = df["algorithm"].str.upper()

# Calculate derived metric: Efficiency = TPS / Energy per Tx
df["efficiency"] = df["realized_tps"] / df["energy_per_tx"]

# Create output directory if not exists
output_dir = "results/graphs_annotated"
os.makedirs(output_dir, exist_ok=True)

# Set seaborn style
sns.set_theme(style="whitegrid", context="talk")

# ------------------------------
# 1. Average Latency Boxplot
# ------------------------------
plt.figure(figsize=(10, 6))
ax = sns.boxplot(x="algorithm", y="avg_latency", data=df, palette="Set2")
plt.title("Average Transaction Latency Across Consensus Algorithms")
plt.xlabel("Consensus Algorithm")
plt.ylabel("Average Latency (seconds)")

# Fix: Label medians accurately by algorithm on actual xtick order
medians = df.groupby("algorithm")["avg_latency"].median().to_dict()
counts = df["algorithm"].value_counts().to_dict()

# Annotate on correct tick positions
for tick, label in enumerate(ax.get_xticklabels()):
    algo = label.get_text()
    median = medians.get(algo, 0)
    count = counts.get(algo, 0)
    ax.text(tick, median + 5, f"{median:.1f}s\n(n={count})", ha="center", fontsize=11)

plt.tight_layout()
plt.savefig(f"{output_dir}/avg_latency_boxplot_annotated.png")
plt.close()

# ------------------------------
# 2. TPS vs Average Latency (per scenario)
# ------------------------------
plt.figure(figsize=(10, 6))
ax = sns.scatterplot(data=df, x="realized_tps", y="avg_latency",
                     hue="algorithm", style="algorithm", s=120, palette="Set2")
for _, row in df.iterrows():
    ax.text(row["realized_tps"] + 0.6, row["avg_latency"] + 1.2,
            row["scenario"], fontsize=9)

plt.title("TPS vs. Average Latency by Scenario")
plt.xlabel("Realized TPS (transactions/sec)")
plt.ylabel("Average Latency (seconds)")
plt.legend(title="Consensus Algorithm")
plt.tight_layout()
plt.savefig(f"{output_dir}/tps_vs_latency_scenarios.png")
plt.close()

# ------------------------------
# 3. Energy Consumption per Transaction
# ------------------------------
plt.figure(figsize=(10, 6))
sns.barplot(x="algorithm", y="energy_per_tx", data=df, errorbar="sd", palette="Set2")
plt.title("Energy Consumption per Transaction")
plt.xlabel("Consensus Algorithm")
plt.ylabel("Energy per Transaction (Joules)")
plt.tight_layout()
plt.savefig(f"{output_dir}/energy_per_tx_barplot.png")
plt.close()

# ------------------------------
# 4. P95 Latency per Scenario
# ------------------------------
plt.figure(figsize=(12, 6))
sns.barplot(x="scenario", y="p95_latency", hue="algorithm", data=df, palette="Set2")
plt.title("95th Percentile Latency per Scenario")
plt.xlabel("Test Scenario")
plt.ylabel("P95 Latency (seconds)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/p95_latency_per_scenario.png")
plt.close()

# ------------------------------
# 5. Transaction Efficiency (TPS per Joule)
# ------------------------------
plt.figure(figsize=(10, 6))
sns.barplot(x="algorithm", y="efficiency", data=df, errorbar="sd", palette="Set2")
plt.title("Transaction Efficiency (TPS per Joule)")
plt.xlabel("Consensus Algorithm")
plt.ylabel("Efficiency (TPS / Joule)")
plt.tight_layout()
plt.savefig(f"{output_dir}/efficiency_barplot.png")
plt.close()

print(f"✅ All final graphs are saved to: {output_dir}")
