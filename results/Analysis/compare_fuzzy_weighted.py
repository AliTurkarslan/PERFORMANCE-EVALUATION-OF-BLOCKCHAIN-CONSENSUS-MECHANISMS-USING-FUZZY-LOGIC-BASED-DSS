import pandas as pd
import os

# 1. Dosyaları yükle
fuzzy_path = "results/fuzzy_prepared/fuzzy_performance_scores.csv"
weighted_path = "results/fuzzy_prepared/weighted_scores.csv"

fuzzy_df = pd.read_csv(fuzzy_path)
weighted_df = pd.read_csv(weighted_path)

# 2. Birleştir
merged = pd.merge(fuzzy_df, weighted_df, on=["algorithm", "scenario"])

# 3. Fark sütununu ekle
merged["difference"] = merged["weighted_score"] - merged["fuzzy_performance"]

# 4. İsteğe bağlı sıralama (senaryo bazlı)
merged = merged.sort_values(by="scenario")

# 5. Sonuçları kaydet
output_path = "results/fuzzy_prepared/score_comparison_table.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged.to_csv(output_path, index=False)

# 6. Ekrana yazdır (isteğe bağlı)
print("✅ Comparison table saved to:", output_path)
print(merged.to_string(index=False))


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("results/fuzzy_prepared/score_comparison_table.csv")

df_melted = df.melt(id_vars=["algorithm", "scenario"],
                    value_vars=["fuzzy_performance", "weighted_score"],
                    var_name="method", value_name="score")

plt.figure(figsize=(12, 6))
sns.barplot(data=df_melted, x="scenario", y="score", hue="method", palette="Set2")
plt.title("Fuzzy vs Weighted Score per Scenario")
plt.ylabel("Score")
plt.xlabel("Scenario")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("results/fuzzy_prepared/fuzzy_vs_weighted_score_per_scenario.png")
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="fuzzy_performance", y="weighted_score", hue="algorithm", style="algorithm", s=120)
plt.plot([0, 1], [0, 1], "--", color="gray")  # Diagonal = eşit skor
plt.title("Fuzzy vs Weighted Score Scatter Plot")
plt.xlabel("Fuzzy Inference Score")
plt.ylabel("Weighted Score")
plt.tight_layout()
plt.savefig("results/fuzzy_prepared/fuzzy_vs_weighted_scatter.png")
plt.show()


