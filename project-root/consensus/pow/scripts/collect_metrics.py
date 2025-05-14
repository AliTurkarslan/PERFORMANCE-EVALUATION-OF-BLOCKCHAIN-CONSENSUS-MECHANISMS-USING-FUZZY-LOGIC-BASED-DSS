from web3 import Web3
import csv
import time
import json
from datetime import datetime
import statistics
import os

# Web3 bağlantısı
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# Girdi dosyası
csv_path = "results/tx_log.csv"
output_path = "results/metrics_summary.json"

# Log dosyasını oku
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    tx_data = {row['tx_hash']: row['submission_time'] for row in reader}

# Metrikleri toplamak için listeler
results = []
total_gas_used = 0
latencies = []

print(f"📊 İşlem sayısı: {len(tx_data)}")

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

        total_gas_used += gas_used
        latencies.append(latency)

# TPS için süreyi hesapla
submission_times = [datetime.fromisoformat(t).timestamp() for t in tx_data.values()]
elapsed_time = max(submission_times) - min(submission_times)
realized_tps = len(results) / elapsed_time if elapsed_time > 0 else 0

# Energy hesaplama: %30 CPU, 50W sistem varsayımı
cpu_percent = 0.30
system_power_watt = 50
estimated_energy_joule = cpu_percent * system_power_watt * elapsed_time
energy_per_tx = estimated_energy_joule / len(results) if results else 0

# Özet metrikler
summary = {
    "total_tx": len(results),
    "avg_gas_used": total_gas_used / len(results) if results else 0,
    "total_gas_used": total_gas_used,
    "avg_latency": statistics.mean(latencies) if latencies else 0,
    "min_latency": min(latencies) if latencies else 0,
    "max_latency": max(latencies) if latencies else 0,
    "p95_latency": statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else max(latencies, default=0),
    "realized_tps": realized_tps,
    "energy_joule_total": estimated_energy_joule,
    "energy_per_tx": energy_per_tx
}

# JSON'a kaydet
os.makedirs("results", exist_ok=True)
with open(output_path, "w") as f:
    json.dump(summary, f, indent=4)

print("✅ Geliştirilmiş metrikler başarıyla toplandı ve kaydedildi:")
print(json.dumps(summary, indent=2))