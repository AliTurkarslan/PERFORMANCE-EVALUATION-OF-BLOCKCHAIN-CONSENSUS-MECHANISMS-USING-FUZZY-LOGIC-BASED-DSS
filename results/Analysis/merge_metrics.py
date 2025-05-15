import os
import json
import pandas as pd

# Base directory containing the consensus algorithm folders
BASE_DIR = "consensus"

# The consensus types you want to merge results for
algorithms = ["poa", "pow", "pos"]

summary_records = []
detailed_records = []

# Iterate through each consensus type
for algo in algorithms:
    result_path = os.path.join(BASE_DIR, algo, "results")
    for scenario in os.listdir(result_path):
        scenario_dir = os.path.join(result_path, scenario)

        # Define file paths
        metrics_file = os.path.join(scenario_dir, "metrics_summary.json")
        tx_detailed_file = os.path.join(scenario_dir, "tx_detailed_log.csv")

        # Parse metrics_summary.json
        if os.path.isfile(metrics_file):
            with open(metrics_file, "r") as f:
                data = json.load(f)
                data["algorithm"] = algo
                data["scenario"] = scenario
                summary_records.append(data)

        # Parse tx_detailed_log.csv
        if os.path.isfile(tx_detailed_file):
            df = pd.read_csv(tx_detailed_file)
            df["algorithm"] = algo
            df["scenario"] = scenario
            detailed_records.append(df)

# Save combined results
summary_df = pd.DataFrame(summary_records)
summary_df.to_csv("all_metrics.csv", index=False)

detailed_df = pd.concat(detailed_records, ignore_index=True)
detailed_df.to_csv("all_tx_detailed.csv", index=False)

print("✅ Combined metrics saved to all_metrics.csv and all_tx_detailed.csv")
