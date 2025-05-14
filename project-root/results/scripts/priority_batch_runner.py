"""
Run DSS inference for all priority combinations.
For each combo, recommend the algorithm that wins most scenarios (highest score per scenario).
"""

import itertools
import subprocess
import pandas as pd
import os

# === 1. Setup ===
levels = ["low", "medium", "high"]
combinations = list(itertools.product(levels, repeat=4))
results_dir = "results/fuzzy_batch"
os.makedirs(results_dir, exist_ok=True)
summary_records = []

print(f"\n🔁 Running DSS for {len(combinations)} priority combinations...\n")

# === 2. Batch execution ===
for i, (lat, p95, tps, energy) in enumerate(combinations, start=1):
    combo_name = f"{lat}_{p95}_{tps}_{energy}"
    output_file = os.path.join(results_dir, f"scores_{combo_name}.csv")

    print(f"▶ [{i}/{len(combinations)}] {combo_name} ... ", end="", flush=True)

    try:
        # Run DSS inference
        cmd = [
            "python3", "results/run_dss_inference.py",
            "--latency", lat,
            "--p95", p95,
            "--tps", tps,
            "--energy", energy
        ]
        subprocess.run(cmd, check=True)

        # Load detailed scores
        src = "results/fuzzy_dss/dss_suitability_scores.csv"
        df = pd.read_csv(src)
        df.to_csv(output_file, index=False)

        # Determine scenario winners
        winners = (
            df.loc[df.groupby("scenario")["suitability_score"].idxmax()]
        )

        winner_counts = winners["algorithm"].value_counts().to_dict()
        best_alg = max(winner_counts, key=winner_counts.get)
        total_scenarios = df["scenario"].nunique()
        win_ratio = winner_counts[best_alg] / total_scenarios

        summary_records.append({
            "priority_latency": lat,
            "priority_p95": p95,
            "priority_tps": tps,
            "priority_energy": energy,
            "recommended_algorithm": best_alg,
            "scenario_wins": winner_counts[best_alg],
            "win_ratio": round(win_ratio, 3)
        })

        print(f"🏆 {best_alg} wins {winner_counts[best_alg]}/{total_scenarios}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

# === 3. Save summary ===
summary_df = pd.DataFrame(summary_records)
summary_path = os.path.join(results_dir, "summary_recommendations.csv")
summary_df.to_csv(summary_path, index=False)

print(f"\n📄 All combinations completed. Summary saved to:\n  {summary_path}")
