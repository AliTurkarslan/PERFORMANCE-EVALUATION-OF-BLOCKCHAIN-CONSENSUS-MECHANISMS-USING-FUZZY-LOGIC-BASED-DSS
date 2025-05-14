#!/bin/bash

# ✅ Manually configure the test scenario
TPS=50
DURATION=60
ACCOUNT="0x578955Ad5eca98bDf98DA7cFA50e887cc38E07b4"
SCENARIO="pow_${TPS}tps"

echo "🛑 Stopping previous PoW network..."
bash scripts/stop_all.sh

echo "🧹 Cleaning previous chain data..."
bash scripts/clean_all.sh

echo "🔧 Initializing chain..."
bash scripts/init_all.sh

echo "🚀 Starting nodes..."
bash scripts/start_all.sh
sleep 20

echo "📦 Deploying smart contract..."
python3 scripts/deploy_contract.py
sleep 5

echo "📤 Sending transactions..."
python3 scripts/generate_transactions.py --tps $TPS --duration $DURATION --account $ACCOUNT --scenario $SCENARIO

echo "📊 Collecting metrics..."
python3 scripts/collect_metrics.py --scenario $SCENARIO

echo "✅ Benchmark complete for: $SCENARIO"
