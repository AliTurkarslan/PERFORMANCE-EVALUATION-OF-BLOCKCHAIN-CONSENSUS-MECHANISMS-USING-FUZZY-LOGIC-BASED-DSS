#!/bin/bash

echo "🚀 Launching 4-node Ethereum PoW network..."

for i in 1 2 3 4
do
  port=$((30302 + $i))         # P2P Port
  rpcport=$((8544 + $i))       # HTTP-RPC Port
  wsport=$((8644 + $i))        # WebSocket Port
  authrpcport=$((8744 + $i))   # Engine API Port

  echo "📡 Starting node $i → P2P: $port | RPC: $rpcport | WS: $wsport | AUTH-RPC: $authrpcport"

  geth --datadir ethereum/node$i \
    --networkid 12345 \
    --port $port \
    --http --http.addr "0.0.0.0" --http.port $rpcport \
    --http.api personal,eth,net,web3,miner \
    --ws --ws.addr "0.0.0.0" --ws.port $wsport \
    --authrpc.port $authrpcport \
    --authrpc.addr "127.0.0.1" \
    --unlock 0 \
    --password config/node${i}_password.txt \
    --allow-insecure-unlock \
    --mine --miner.threads=1 \
    --nodiscover \
    --ipcdisable \
    --verbosity 3 >> log/geth_node$i.log 2>&1 &

  sleep 1
done

echo "✅ All nodes launched. Check logs in 'log/' folder."
