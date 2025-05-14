#!/bin/bash

echo "🛑 Stopping all Geth nodes..."

# Node dizinlerini sırayla kontrol edip durdur
for i in {1..4}
do
    # İlgili node için çalışıp çalışmadığını kontrol et
    PID=$(ps aux | grep "ethereum/node$i" | grep geth | awk '{print $2}')

    if [ -z "$PID" ]; then
        echo "⚠️  Node$i is not running."
    else
        echo "🔻 Stopping node$i (PID: $PID)..."
        kill -INT $PID
        sleep 2
    fi
done

echo "✅ All nodes attempted to stop."
