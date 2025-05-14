from scipy.stats import wilcoxon
import pandas as pd

df = pd.read_csv("results/fuzzy_prepared/score_comparison_table.csv")

# Wilcoxon test (eşleşmiş)
stat, p = wilcoxon(df["fuzzy_performance"], df["weighted_score"])
print(f"Wilcoxon Signed-Rank Test p-value: {p:.4f}")
