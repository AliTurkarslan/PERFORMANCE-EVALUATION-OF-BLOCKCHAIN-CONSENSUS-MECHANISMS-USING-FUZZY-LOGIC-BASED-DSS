"""
run_classical_scoring.py
Calculates classical weighted scores for all user priority combinations (low/med/high).
Saves per-combination scores and a recommendation summary like fuzzy system.
"""

import pandas as pd
import itertools
import os

# === 1. Load normalized metrics ===
metrics_path = "data/normalized_metrics.csv"
df = pd.read_csv(metrics_path)

# === 2. Priority to weight mapping ===
priority_to_weight = {"low": 0.1, "medium": 0.3, "high": 0.5}

# === 3. Prepare output folders ===
out_dir = "results/classical_batch"
os.makedirs(out_dir, exist_ok=True)

summary = []

# === 4. Generate all combinations ===
levels = ["low", "medium", "high"]
combinations = list(itertools.product(levels, repeat=4))

print(f"📊 Running classical scoring for {len(combinations)} combinations...")

# === 5. Scoring function ===
def compute_score(row, weights):
    return (
        (row["norm_latency"]) * weights[0] +
        (row["norm_p95"]) * weights[1] +
        row["norm_tps"] * weights[2] +
        (row["norm_energy"]) * weights[3]
    )

# === 6. Loop through combinations ===
for i, (lat, p95, tps, energy) in enumerate(combinations, start=1):
    combo = f"{lat}_{p95}_{tps}_{energy}"
    print(f"[{i:02}/{len(combinations)}] → {combo}")

    weights = (
        priority_to_weight[lat],
        priority_to_weight[p95],
        priority_to_weight[tps],
        priority_to_weight[energy]
    )

    temp_df = df.copy()
    temp_df["classical_score"] = temp_df.apply(lambda r: compute_score(r, weights), axis=1)
    temp_df.to_csv(f"{out_dir}/scores_{combo}.csv", index=False)

    winners = temp_df.loc[temp_df.groupby("scenario")["classical_score"].idxmax()]
    win_counts = winners["algorithm"].value_counts().to_dict()
    best_alg = max(win_counts, key=win_counts.get)
    win_total = temp_df["scenario"].nunique()

    summary.append({
        "priority_latency": lat,
        "priority_p95": p95,
        "priority_tps": tps,
        "priority_energy": energy,
        "recommended_algorithm": best_alg,
        "scenario_wins": win_counts[best_alg],
        "win_ratio": round(win_counts[best_alg] / win_total, 3)
    })

# === 7. Save summary ===
summary_df = pd.DataFrame(summary)
summary_df.to_csv(f"{out_dir}/summary_recommendations.csv", index=False)

print(f"\n✅ All classical scoring complete. Summary saved to:\n  {out_dir}/summary_recommendations.csv")
