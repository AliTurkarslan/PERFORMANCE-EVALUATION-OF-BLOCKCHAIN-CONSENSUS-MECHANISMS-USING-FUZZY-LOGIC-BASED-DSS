import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Setup ===
input_file = "results/fuzzy_prepared/fuzzy_scores.csv"
output_dir = "results/fuzzy_prepared"
os.makedirs(output_dir, exist_ok=True)

# === Load fuzzy scores ===
df = pd.read_csv(input_file)

# === STRATEGY 1: Scenario-based Best Algorithm ===
best_per_scenario = df.loc[df.groupby("scenario")["fuzzy_score"].idxmax()].reset_index(drop=True)
best_per_scenario.to_csv(f"{output_dir}/best_per_scenario.csv", index=False)

plt.figure(figsize=(10, 5))
sns.barplot(data=best_per_scenario, x="scenario", y="fuzzy_score", hue="algorithm", palette="Set2")
plt.title("Strategy 1: Best Performing Algorithm per Scenario")
plt.ylabel("Fuzzy Score")
plt.xlabel("Test Scenario")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/strategy1_best_per_scenario.png")
plt.close()

# === STRATEGY 2: Global Average per Algorithm ===
avg_scores = df.groupby("algorithm")["fuzzy_score"].mean().reset_index()
avg_scores = avg_scores.sort_values(by="fuzzy_score", ascending=False)
avg_scores.to_csv(f"{output_dir}/algorithm_average_scores.csv", index=False)

plt.figure(figsize=(8, 5))
sns.barplot(data=avg_scores, x="algorithm", y="fuzzy_score", palette="Set2")
plt.title("Strategy 2: Global Average Score per Algorithm")
plt.ylabel("Average Fuzzy Score")
plt.xlabel("Consensus Algorithm")
plt.tight_layout()
plt.savefig(f"{output_dir}/strategy2_average_scores.png")
plt.close()

print("✅ Decision Strategy outputs created:")
print(" • best_per_scenario.csv")
print(" • strategy1_best_per_scenario.png")
print(" • algorithm_average_scores.csv")
print(" • strategy2_average_scores.png")
