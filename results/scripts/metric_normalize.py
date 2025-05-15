import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# === 1. Load original raw metrics ===
df = pd.read_csv("results/all_metrics.csv")
df["algorithm"] = df["algorithm"].str.upper()
df["scenario"] = df["scenario"].str.lower()

# === 2. Extract relevant metrics ===
metrics = df[["avg_latency", "p95_latency", "realized_tps", "energy_per_tx"]].copy()

# === 3. Z-score normalization ===
z = (metrics - metrics.mean()) / metrics.std()

# === 4. Invert metrics where lower is better ===
z["avg_latency"] = -z["avg_latency"]
z["p95_latency"] = -z["p95_latency"]
z["energy_per_tx"] = -z["energy_per_tx"]
# TPS is already higher = better

# === 5. Min-Max normalize to [0.05, 0.95] to avoid fuzzy overflow ===
scaler = MinMaxScaler(feature_range=(0.05, 0.95))
scaled_array = scaler.fit_transform(z)
scaled_df = pd.DataFrame(scaled_array, columns=["norm_latency", "norm_p95", "norm_tps", "norm_energy"])

# === 6. Combine with identifiers ===
final_df = pd.concat([df[["algorithm", "scenario"]], scaled_df], axis=1)

# === 7. Save output ===
out_dir = "results/fuzzy_prepared"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "normalized_metrics.csv")
final_df.to_csv(out_path, index=False)

print(f"✅ Normalized fuzzy metrics (z-score + minmax) saved to: {out_path}")
