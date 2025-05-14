import pandas as pd
import os

# Load normalized data
df = pd.read_csv("results/fuzzy_prepared/normalized_metrics.csv")

# Ağırlıkları uygula
df["weighted_score"] = (
    df["norm_latency"] * 0.3 +
    df["norm_p95"] * 0.2 +
    df["norm_tps"] * 0.3 +
    df["norm_energy"] * 0.2
)

# Sonuçları kaydet
os.makedirs("results/fuzzy_prepared", exist_ok=True)
df[["algorithm", "scenario", "weighted_score"]].to_csv("results/fuzzy_prepared/weighted_scores.csv", index=False)

print("✅ Weighted scores saved to results/fuzzy_prepared/weighted_scores.csv")
