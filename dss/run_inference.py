"""
run_inference.py
Runs the Fuzzy DSS system for a single set of user-defined priorities.
Generates suitability scores for each algorithm-scenario pair.
"""

import argparse
import os
import pandas as pd
import numpy as np
from dss.define_fuzzy_dss import create_dss_system

# === 1. Parse user-defined priorities ===
parser = argparse.ArgumentParser(description="Run Fuzzy DSS for a specific priority configuration.")
parser.add_argument("--latency", choices=["low", "medium", "high"], default="medium")
parser.add_argument("--p95", choices=["low", "medium", "high"], default="medium")
parser.add_argument("--tps", choices=["low", "medium", "high"], default="medium")
parser.add_argument("--energy", choices=["low", "medium", "high"], default="medium")
args = parser.parse_args()

priority_map = {"low": 0.1, "medium": 0.55, "high": 0.95}
user_priorities = {
    "priority_latency": priority_map[args.latency],
    "priority_p95": priority_map[args.p95],
    "priority_tps": priority_map[args.tps],
    "priority_energy": priority_map[args.energy]
}

print("\n🔧 User priorities:")
for k, v in user_priorities.items():
    print(f"  - {k}: {v:.2f}")

# === 2. Load normalized metrics ===
metric_file = "data/normalized_metrics.csv"
if not os.path.exists(metric_file):
    raise FileNotFoundError(f"❌ Metrics file not found: {metric_file}")

df = pd.read_csv(metric_file)
required_cols = {"algorithm", "scenario", "norm_latency", "norm_p95", "norm_tps", "norm_energy"}
if not required_cols.issubset(df.columns):
    raise ValueError("❌ Input file is missing required columns.")

# === 3. Clamp helper for fuzzy input safety ===
def clamp(x):
    return min(0.999, max(0.001, float(x)))

# === 4. Run DSS simulation for each row ===
results = []
for _, row in df.iterrows():
    sim = create_dss_system()
    try:
        # Set normalized performance inputs
        sim.input['latency_value'] = clamp(row['norm_latency'])
        sim.input['p95_value'] = clamp(row['norm_p95'])
        sim.input['tps_value'] = clamp(row['norm_tps'])
        sim.input['energy_value'] = clamp(row['norm_energy'])

        # Set user-defined priorities
        sim.input['priority_latency'] = clamp(user_priorities['priority_latency'])
        sim.input['priority_p95'] = clamp(user_priorities['priority_p95'])
        sim.input['priority_tps'] = clamp(user_priorities['priority_tps'])
        sim.input['priority_energy'] = clamp(user_priorities['priority_energy'])

        sim.compute()
        score = sim.output.get("suitability", np.nan)

    except Exception as e:
        print(f"⚠️ Error processing {row['algorithm']} - {row['scenario']}: {e}")
        score = np.nan

    results.append({
        "algorithm": row["algorithm"],
        "scenario": row["scenario"],
        "suitability_score": score
    })

# === 5. Save output ===
output_dir = "results/fuzzy_dss"
os.makedirs(output_dir, exist_ok=True)
out_path = os.path.join(output_dir, "dss_suitability_scores.csv")

pd.DataFrame(results).to_csv(out_path, index=False)
print(f"\n✅ Suitability scores saved to: {out_path}")
