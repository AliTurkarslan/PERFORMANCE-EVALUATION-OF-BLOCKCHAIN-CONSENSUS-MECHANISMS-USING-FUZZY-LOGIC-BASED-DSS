import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load normalized metrics
df = pd.read_csv("results/fuzzy_prepared/normalized_metrics.csv")

# Define weights for each metric
weights = {
    "norm_latency": 0.3,
    "norm_p95": 0.2,
    "norm_tps": 0.3,
    "norm_energy": 0.2
}

# Compute weighted fuzzy score
df["fuzzy_score"] = (
    df["norm_latency"] * weights["norm_latency"] +
    df["norm_p95"] * weights["norm_p95"] +
    df["norm_tps"] * weights["norm_tps"] +
    df["norm_energy"] * weights["norm_energy"]
)

# Save final scores
os.makedirs("results/fuzzy_prepared", exist_ok=True)
df.to_csv("results/fuzzy_prepared/fuzzy_scores.csv", index=False)

# Plot fuzzy score by scenario
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x="scenario", y="fuzzy_score", hue="algorithm", palette="Set2")
plt.title("Fuzzy Logic Score per Scenario")
plt.ylabel("Fuzzy Score (0 to 1)")
plt.xlabel("Test Scenario")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("results/fuzzy_prepared/fuzzy_scores_barplot.png")
plt.close()

print("✅ Fuzzy scores calculated and saved.")
