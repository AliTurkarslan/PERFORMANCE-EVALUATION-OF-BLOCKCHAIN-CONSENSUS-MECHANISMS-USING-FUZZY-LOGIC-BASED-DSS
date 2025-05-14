import pandas as pd
from define_fuzzy_system import create_fuzzy_system
import numpy as np

df = pd.read_csv("results/fuzzy_prepared/normalized_metrics.csv")
results = []

# Güvenli normalize değeri: 0.0–1.0 sınırında kalan uç noktaları içeri çeker
safe = lambda x: min(0.999, max(0.001, float(x)))  # float eklemek NaN hatalarına karşı da korur

for _, row in df.iterrows():
    sim = create_fuzzy_system()
    try:
        sim.input['latency'] = safe(row["norm_latency"])
        sim.input['p95'] = safe(row["norm_p95"])
        sim.input['tps'] = safe(row["norm_tps"])
        sim.input['energy'] = safe(row["norm_energy"])
        sim.compute()
        output = sim.output.get("performance", np.nan)
    except Exception as e:
        print(f"⚠️ Warning: simulation failed for {row['scenario']} ({row['algorithm']}): {e}")
        output = np.nan

    results.append({
        "algorithm": row["algorithm"],
        "scenario": row["scenario"],
        "fuzzy_performance": output
    })

pd.DataFrame(results).to_csv("results/fuzzy_prepared/fuzzy_performance_scores.csv", index=False)
print("✅ Fuzzy inference scores saved.")
