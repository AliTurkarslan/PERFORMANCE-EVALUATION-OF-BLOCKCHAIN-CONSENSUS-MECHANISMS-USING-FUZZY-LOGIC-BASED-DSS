import argparse
from web3 import Web3
import csv
import time
import json
from datetime import datetime
import statistics
import os

# 🛠️ CLI Arguments
parser = argparse.ArgumentParser(description="Collect benchmark metrics")
parser.add_argument("--scenario", type=str, required=True, help="Scenario name (e.g., pow_500tps)")
args = parser.parse_args()

SCENARIO = args.scenario
TX_LOG_PATH = f"results/{SCENARIO}/tx_log.csv"
METRICS_OUTPUT_PATH = f"results/{SCENARIO}/metrics_summary.json"

# ✅ Connect to Ethereum Node
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# ✅ Load transaction log
with open(TX_LOG_PATH, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    tx_data = {row['tx_hash']: row['submission_time'] for row in reader}

print(f"📊 Total Transactions Logged: {len(tx_data)}")

# ✅ Collect metrics
results = []
gas_values = []
latencies = []

for tx_hash, sent_time_str in tx_data.items():
    receipt = None
    retry = 0
    while receipt is None and retry < 10:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
        except:
            time.sleep(1)
            retry += 1

    if receipt:
        sent_time = datetime.fromisoformat(sent_time_str).timestamp()
        mined_time = w3.eth.get_block(receipt.blockNumber).timestamp
        latency = mined_time - sent_time
        gas_used = receipt.gasUsed

        results.append({
            "tx_hash": tx_hash,
            "block": receipt.blockNumber,
            "gas_used": gas_used,
            "latency": latency
        })

        gas_values.append(gas_used)
        latencies.append(latency)

# ✅ Calculate metrics
success_tx = len(results)
submission_times = [datetime.fromisoformat(t).timestamp() for t in tx_data.values()]
elapsed_time = max(submission_times) - min(submission_times)
realized_tps = success_tx / elapsed_time if elapsed_time > 0 else 0

CPU_UTILIZATION = 0.30
SYSTEM_POWER_WATT = 50
estimated_energy_joule = CPU_UTILIZATION * SYSTEM_POWER_WATT * elapsed_time
energy_per_tx = estimated_energy_joule / success_tx if success_tx else 0

summary = {
    "total_tx": len(tx_data),
    "success_tx": success_tx,
    "realized_tps": realized_tps,
    "avg_latency": statistics.mean(latencies) if latencies else 0,
    "p95_latency": statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else max(latencies, default=0),
    "latency_variance": statistics.variance(latencies) if len(latencies) > 1 else 0,
    "avg_gas_used": statistics.mean(gas_values) if gas_values else 0,
    "total_gas_used": sum(gas_values),
    "gas_std_dev": statistics.stdev(gas_values) if len(gas_values) > 1 else 0,
    "energy_joule_total": estimated_energy_joule,
    "energy_per_tx": energy_per_tx
}

# ✅ Save output
os.makedirs(f"results/{SCENARIO}", exist_ok=True)
with open(METRICS_OUTPUT_PATH, "w") as f:
    json.dump(summary, f, indent=4)

print("✅ Metrics successfully collected and saved:")
print(json.dumps(summary, indent=2))
