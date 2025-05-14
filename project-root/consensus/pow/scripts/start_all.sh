#!/bin/bash

echo "🚀 Launching 4-node Ethereum PoW network..."

for i in 1 2 3 4
do
  port=$((30302 + $i))         # P2P ports: 30303, 30304, 30305, 30306
  rpcport=$((8544 + $i))       # RPC ports: 8545, 8546, 8547, 8548

  echo "📡 Starting node $i → P2P Port: $port | RPC Port: $rpcport"

  geth --datadir ethereum/node$i \
    --networkid 12345 \
    --port $port \
    --http --http.addr "0.0.0.0" --http.port $rpcport \
    --http.api personal,eth,net,web3,miner \
    --unlock 0 \
    --password config/node${i}_password.txt \
    --allow-insecure-unlock \
    --mine --miner.threads=1 \
    --nodiscover \
    --ipcdisable \
    --verbosity 3 >> log/geth_node$i.log 2>&1 &

  sleep 1
done

echo "✅ All nodes started successfully. Check logs in the 'log/' folder."