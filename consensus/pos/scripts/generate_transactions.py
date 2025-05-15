import argparse
from web3 import Web3
import json
import csv
import os
import time
from datetime import datetime, timezone
from web3.middleware import geth_poa_middleware

# 🛠️ CLI Arguments
parser = argparse.ArgumentParser(description="Generate transactions for benchmark")
parser.add_argument("--tps", type=int, required=True, help="Transactions per second")
parser.add_argument("--duration", type=int, default=60, help="Test duration in seconds")
parser.add_argument("--port", type=int, default=8545, help="Ethereum RPC port (default: 8545)")
parser.add_argument("--account", type=str, required=True, help="Sender account address")
parser.add_argument("--scenario", type=str, required=True, help="Scenario name (e.g., pow_500tps)")
args = parser.parse_args()

TPS = args.tps
DURATION = args.duration
PORT = args.port
FROM_ACCOUNT = args.account
SCENARIO = args.scenario
TOTAL_TX = TPS * DURATION

# ✅ Connect to Ethereum Node
w3 = Web3(Web3.HTTPProvider(f"http://127.0.0.1:{PORT}"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.default_account = FROM_ACCOUNT

if not w3.is_connected():
    print(f"❌ Could not connect to Ethereum node at port {PORT}")
    exit(1)

# ✅ Load ABI & Address
with open("build/kvstore.abi") as f:
    abi = json.load(f)

with open("log/contract_address.txt") as f:
    contract_address = f.read().strip()

contract = w3.eth.contract(address=contract_address, abi=abi)

# ✅ Prepare CSV log
os.makedirs(f"results/{SCENARIO}", exist_ok=True)
log_path = f"results/{SCENARIO}/tx_log.csv"

with open(log_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["tx_index", "tx_hash", "submission_time"])

    print(f"🚀 Sending {TOTAL_TX} transactions at {TPS} TPS from {FROM_ACCOUNT} ({SCENARIO})...\n")

    for i in range(TOTAL_TX):
        key = f"user_{i}"
        value = f"value_{i}"
        latest_block_ts = w3.eth.get_block("latest").timestamp
        timestamp = datetime.fromtimestamp(latest_block_ts + 1, timezone.utc).isoformat()

        try:
            tx_hash = contract.functions.set(key, value).transact({
                "from": FROM_ACCOUNT,
                "gas": 300000,
                "gasPrice": Web3.to_wei(1, "gwei")
            })
            writer.writerow([i, tx_hash.hex(), timestamp])
            csvfile.flush()
            print(f"[{i}] TX sent → {tx_hash.hex()} at {timestamp}")
        except Exception as e:
            print(f"[{i}] ❌ Error sending transaction: {str(e)}")

        time.sleep(1 / TPS)

print(f"\n✅ Test complete. Transaction log saved to: {log_path}")


