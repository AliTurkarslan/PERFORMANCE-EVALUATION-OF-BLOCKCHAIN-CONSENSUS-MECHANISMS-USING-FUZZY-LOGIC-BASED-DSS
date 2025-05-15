#!/bin/bash

echo "🚀 Launching 4-node Ethereum PoA network..."

# Explicit signer addresses
declare -a SIGNERS=(
  "0x578955Ad5eca98bDf98DA7cFA50e887cc38E07b4"
  "0x6002Fb13A09dE998abfc73c1F2C4B21585710b9E"
  "0x39eb96A913b3DF172c60371F78483993618eC09D"
  "0x68d8164C163A5E0C001c1A66293e5E128Ffc7DA4"
)

for i in 1 2 3 4
do
  port=$((30302 + $i))
  rpcport=$((8544 + $i))
  wsport=$((8644 + $i))
  authrpcport=$((8744 + $i))

  echo "📡 Starting node $i → P2P: $port | RPC: $rpcport | WS: $wsport | AUTH-RPC: $authrpcport"

  geth --datadir ethereum/node$i \
    --networkid 54321 \
    --port $port \
    --syncmode full \
    --http --http.addr "0.0.0.0" --http.port $rpcport \
    --http.api personal,eth,net,web3,miner \
    --ws --ws.addr "0.0.0.0" --ws.port $wsport \
    --authrpc.port $authrpcport \
    --authrpc.addr "127.0.0.1" \
    --unlock "${SIGNERS[$((i - 1))]}" \
    --password config/node${i}_password.txt \
    --allow-insecure-unlock \
    --mine --miner.threads=1 \
    --nodiscover \
    --ipcdisable \
    --verbosity 3 >> log/geth_node$i.log 2>&1 &

  sleep 1
done

echo "✅ All nodes launched. Check logs in 'log/' folder."
