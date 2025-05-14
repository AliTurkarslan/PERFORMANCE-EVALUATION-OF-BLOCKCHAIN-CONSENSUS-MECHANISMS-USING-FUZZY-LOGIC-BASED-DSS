import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import shapiro

# === 0. Setup ===
df = pd.read_csv("results/all_tx_detailed.csv")
df["submission_time"] = pd.to_datetime(df["submission_time"], utc=True)
df["block_timestamp"] = pd.to_datetime(df["block_timestamp"], utc=True)
df["latency"] = pd.to_numeric(df["latency"], errors="coerce")
df["algorithm"] = df["algorithm"].str.upper()
df["block_time"] = (df["block_timestamp"] - df["submission_time"]).dt.total_seconds()

output_dir = "results/tx_analysis_final"
os.makedirs(output_dir, exist_ok=True)

# === 1. Boxplot: Latency Distribution per Algorithm ===
def plot_latency_distribution():
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="algorithm", y="latency", palette="Set2")
    plt.title("Latency Distribution per Consensus Algorithm")
    plt.xlabel("Consensus Algorithm")
    plt.ylabel("Latency (seconds)")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/latency_distribution_boxplot.png")
    plt.close()

# === 2. Histogram + KDE per Scenario ===
def plot_latency_histograms():
    for scenario in df["scenario"].unique():
        subset = df[df["scenario"] == scenario]
        plt.figure(figsize=(8, 4))
        sns.histplot(subset["latency"], kde=True, bins=30, color="steelblue")
        plt.title(f"Latency Histogram – {scenario}")
        plt.xlabel("Latency (seconds)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/latency_hist_{scenario}.png")
        plt.close()

# === 3. Summary Table per Algorithm & Scenario ===
def latency_summary():
    summary = df.groupby(["algorithm", "scenario"])["latency"].agg(
        count="count",
        mean="mean",
        median="median",
        std="std",
        min="min",
        max="max",
        p95=lambda x: x.quantile(0.95)
    ).reset_index()
    summary.to_csv(f"{output_dir}/latency_summary.csv", index=False)


# === 4. Estimated Block Time per Algorithm ===
def plot_block_time_distribution():
    blocks = df.groupby(["algorithm", "block_number"])["block_timestamp"].min().reset_index()
    blocks = blocks.sort_values(["algorithm", "block_number"])
    blocks["block_time_diff"] = blocks.groupby("algorithm")["block_timestamp"].diff().dt.total_seconds()
    blocks = blocks.dropna()

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=blocks, x="algorithm", y="block_time_diff", palette="Set2")
    plt.title("Estimated Block Time per Consensus Algorithm")
    plt.xlabel("Consensus Algorithm")
    plt.ylabel("Block Time Difference (seconds)")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/block_time_boxplot.png")
    plt.close()

# === 5. Execute All ===
if __name__ == "__main__":
    plot_latency_distribution()
    plot_latency_histograms()
    latency_summary()
    plot_block_time_distribution()
    print("✅ All analysis steps completed and saved to:", output_dir)
