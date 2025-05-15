import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your metrics data
df = pd.read_csv("results/all_metrics.csv")  # Dosyanın doğru adı ve yolu burada!

# Set plot style
sns.set(style="whitegrid")
palette = "Set2"

# 1. Realized TPS Comparison
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="algorithm", y="realized_tps", ci=None, palette=palette)
plt.title("Realized TPS by Consensus Algorithm")
plt.ylabel("Transactions per Second")
plt.xlabel("Algorithm")
plt.tight_layout()
plt.savefig("fig_tps_comparison.png")

# 2. Average Latency Comparison
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="algorithm", y="avg_latency", ci=None, palette=palette)
plt.title("Average Latency by Consensus Algorithm")
plt.ylabel("Latency (seconds)")
plt.xlabel("Algorithm")
plt.tight_layout()
plt.savefig("fig_latency_comparison.png")

# 3. Energy Consumption per Transaction
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="algorithm", y="energy_per_tx", ci=None, palette=palette)
plt.title("Energy Usage per Transaction")
plt.ylabel("Energy (Joules/tx)")
plt.xlabel("Algorithm")
plt.tight_layout()
plt.savefig("fig_energy_per_tx.png")

# 4. Latency Variance
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="algorithm", y="latency_variance", ci=None, palette=palette)
plt.title("Latency Variance")
plt.ylabel("Variance")
plt.xlabel("Algorithm")
plt.tight_layout()
plt.savefig("fig_latency_variance.png")

# 5. Average Block Time
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="algorithm", y="avg_block_time", ci=None, palette=palette)
plt.title("Average Block Time")
plt.ylabel("Block Interval (s)")
plt.xlabel("Algorithm")
plt.tight_layout()
plt.savefig("fig_block_time.png")

# 6. DSS-Based Suitability Score (if available)
try:
    dss_scores = pd.read_csv("results/fuzzy_dss/dss_suitability_scores.csv")
    avg_scores = dss_scores.groupby("algorithm")["suitability_score"].mean().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=avg_scores, x="algorithm", y="suitability_score", palette="crest")
    plt.title("Average DSS Suitability Score per Algorithm")
    plt.ylabel("Suitability Score")
    plt.xlabel("Algorithm")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig("fig_dss_score_comparison.png")
except:
    print("No DSS score file found, skipping DSS plot.")
