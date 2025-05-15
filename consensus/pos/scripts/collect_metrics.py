from web3 import Web3
from web3.middleware import geth_poa_middleware
import argparse
import csv
import time
import json
import os
import statistics
from datetime import datetime

def collect_metrics(scenario, provider="http://localhost:8545"):
    """
    Collects benchmarking metrics from a simulated Ethereum PoS environment.
    Also writes a detailed log per transaction to tx_detailed_log.csv.
    """
    w3 = Web3(Web3.HTTPProvider(provider))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    tx_log_path = f"results/{scenario}/tx_log.csv"
    metrics_output_path = f"results/{scenario}/metrics_summary.json"
    detailed_log_path = f"results/{scenario}/tx_detailed_log.csv"

    with open(tx_log_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        tx_data = {row['tx_hash']: row['submission_time'] for row in reader}

    latencies = []
    gas_values = []
    block_times = {}
    detailed_logs = []

    for i, (tx_hash, sent_time_str) in enumerate(tx_data.items()):
        receipt = None
        for _ in range(10):
            try:
                receipt = w3.eth.get_transaction_receipt(tx_hash)
                break
            except:
                time.sleep(1)

        if receipt:
            sent_time = datetime.fromisoformat(sent_time_str).timestamp()
            block = w3.eth.get_block(receipt.blockNumber)
            latency = max(block.timestamp - sent_time, 0)
            gas = receipt.gasUsed

            latencies.append(latency)
            gas_values.append(gas)

            if receipt.blockNumber not in block_times:
                block_times[receipt.blockNumber] = block.timestamp

            detailed_logs.append({
                "tx_index": i,
                "tx_hash": tx_hash,
                "block_number": receipt.blockNumber,
                "submission_time": sent_time_str,
                "block_timestamp": datetime.utcfromtimestamp(block.timestamp).isoformat(),
                "latency": latency,
                "gas_used": gas,
                "status": receipt.status
            })

    success_tx = len(latencies)
    submission_times = [datetime.fromisoformat(t).timestamp() for t in tx_data.values()]
    elapsed_time = max(submission_times) - min(submission_times)
    realized_tps = success_tx / elapsed_time if elapsed_time > 0 else 0
    success_rate = success_tx / len(tx_data) if tx_data else 0

    if len(block_times) > 1:
        sorted_times = sorted(block_times.items())
        intervals = [t2 - t1 for (_, t1), (_, t2) in zip(sorted_times, sorted_times[1:])]
        avg_block_time = statistics.mean(intervals)
    else:
        avg_block_time = None

    CPU_UTILIZATION = 0.3
    POWER_WATT = 50
    total_energy = CPU_UTILIZATION * POWER_WATT * elapsed_time
    energy_per_tx = total_energy / success_tx if success_tx else 0

    summary = {
        "total_tx": len(tx_data),
        "success_tx": success_tx,
        "success_rate": success_rate,
        "realized_tps": realized_tps,
        "avg_latency": statistics.mean(latencies) if latencies else 0,
        "p95_latency": statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else max(latencies, default=0),
        "latency_variance": statistics.variance(latencies) if len(latencies) > 1 else 0,
        "avg_gas_used": statistics.mean(gas_values) if gas_values else 0,
        "total_gas_used": sum(gas_values),
        "gas_std_dev": statistics.stdev(gas_values) if len(gas_values) > 1 else 0,
        "avg_block_time": avg_block_time,
        "energy_joule_total": total_energy,
        "energy_per_tx": energy_per_tx
    }

    os.makedirs(f"results/{scenario}", exist_ok=True)

    with open(metrics_output_path, "w") as f:
        json.dump(summary, f, indent=4)

    with open(detailed_log_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=detailed_logs[0].keys())
        writer.writeheader()
        writer.writerows(detailed_logs)

    print(f"✅ PoS metrics summary saved to: {metrics_output_path}")
    print(f"✅ PoS detailed log saved to: {detailed_log_path}")
    return summary

# CLI Entry
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect benchmark metrics for Ethereum PoS scenario")
    parser.add_argument("--scenario", type=str, required=True, help="Scenario name (e.g., pos_500tps)")
    args = parser.parse_args()
    collect_metrics(args.scenario)
