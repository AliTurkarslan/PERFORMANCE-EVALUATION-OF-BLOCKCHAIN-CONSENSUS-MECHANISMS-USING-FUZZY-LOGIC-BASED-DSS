#!/bin/bash

echo "🚀 All nodes are starting with genesis..."

for i in 1 2 3 4
do
  echo "🔧 ethereum/node$i dizininde genesis init ediliyor..."
  geth --datadir ethereum/node$i init genesis/CustomGenesis.json
done

echo "✅ All nodes are started."