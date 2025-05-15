"""
run_batch_inference.py
Runs DSS inference across all user priority combinations.
For each combo, identifies the algorithm that wins most scenarios.
Stores per-combination recommendations in a summary CSV.
"""

import os
import itertools
import subprocess
import pandas as pd

# === 1. Define priority levels and combinations ===
levels = ["low", "medium", "high"]
combinations = list(itertools.product(levels, repeat=4))  # 81 total
results_dir = "results/fuzzy_batch"
os.makedirs(results_dir, exist_ok=True)

summary = []

print(f"\n🔁 Running DSS for {len(combinations)} priority combinations...\n")

# === 2. Run each combination ===
for i, (lat, p95, tps, energy) in enumerate(combinations, start=1):
    combo_str = f"{lat}_{p95}_{tps}_{energy}"
    output_file = os.path.join(results_dir, f"scores_{combo_str}.csv")

    print(f"▶ [{i:02}/{len(combinations)}] {combo_str} ... ", end="")

    try:
        # Call the inference script
        cmd = [
            "python3", "dss/run_inference.py",
            "--latency", lat,
            "--p95", p95,
            "--tps", tps,
            "--energy", energy
        ]
        subprocess.run(cmd, check=True)

        # Read output from DSS
        dss_path = "results/fuzzy_dss/dss_suitability_scores.csv"
        df = pd.read_csv(dss_path)
        df.to_csv(output_file, index=False)

        # Winner per scenario
        winners = df.loc[df.groupby("scenario")["suitability_score"].idxmax()]
        win_counts = winners["algorithm"].value_counts().to_dict()

        best_alg = max(win_counts, key=win_counts.get)
        total = df["scenario"].nunique()
        best_count = win_counts[best_alg]
        win_ratio = round(best_count / total, 3)

        summary.append({
            "priority_latency": lat,
            "priority_p95": p95,
            "priority_tps": tps,
            "priority_energy": energy,
            "recommended_algorithm": best_alg,
            "scenario_wins": best_count,
            "win_ratio": win_ratio
        })

        print(f"✅ {best_alg} wins {best_count}/{total} scenarios")

    except Exception as e:
        print(f"❌ ERROR: {e}")

# === 3. Save summary ===
summary_df = pd.DataFrame(summary)
summary_path = os.path.join(results_dir, "summary_recommendations.csv")
summary_df.to_csv(summary_path, index=False)

print(f"\n📄 All combinations completed. Summary saved to:\n  {summary_path}")
