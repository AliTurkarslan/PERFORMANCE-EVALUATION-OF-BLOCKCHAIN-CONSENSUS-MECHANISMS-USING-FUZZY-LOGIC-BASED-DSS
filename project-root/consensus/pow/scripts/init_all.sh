#!/bin/bash

echo "🚀 Node'lar genesis ile başlatılıyor..."

for i in 1 2 3 4
do
  echo "🔧 ethereum/node$i dizininde genesis init ediliyor..."
  geth --datadir ethereum/node$i init genesis/CustomGenesis.json
done

echo "✅ Tüm node'lar genesis ile başarıyla başlatıldı."