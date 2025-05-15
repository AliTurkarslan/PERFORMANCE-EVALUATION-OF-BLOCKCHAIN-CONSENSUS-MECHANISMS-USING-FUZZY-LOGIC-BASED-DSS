#!/bin/bash

echo "🚀 Launching 4-node Ethereum PoS (simulated) network..."

for i in 1 2 3 4
do
  port=$((30302 + $i))         # P2P Port
  rpcport=$((8544 + $i))       # HTTP-RPC Port
  wsport=$((8644 + $i))        # WebSocket Port
  authrpcport=$((8744 + $i))   # Engine API Port

  echo "📡 Starting node $i → P2P: $port | RPC: $rpcport | WS: $wsport | AUTH-RPC: $authrpcport"

  # 🔐 Sadece node1 madenci olacak
  if [[ "$i" -eq 1 ]]; then
    MINE_FLAGS="--mine --miner.threads=1"
  else
    MINE_FLAGS=""
  fi

  geth --datadir ethereum/node$i \
    --networkid 65432 \
    --port $port \
    --http --http.addr "0.0.0.0" --http.port $rpcport \
    --http.api personal,eth,net,web3,miner \
    --ws --ws.addr "0.0.0.0" --ws.port $wsport \
    --authrpc.port $authrpcport \
    --authrpc.addr "127.0.0.1" \
    --unlock 0 \
    --password config/node${i}_password.txt \
    --allow-insecure-unlock \
    $MINE_FLAGS \
    --nodiscover \
    --ipcdisable \
    --verbosity 3 >> log/geth_node$i.log 2>&1 &

  sleep 1
done

echo "✅ All PoS nodes launched. Only Node1 is mining (simulated validator)."
