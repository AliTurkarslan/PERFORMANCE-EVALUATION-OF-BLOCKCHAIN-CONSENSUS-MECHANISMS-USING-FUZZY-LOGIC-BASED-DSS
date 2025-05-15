#!/bin/bash

echo "🧹 Cleaning all geth node data..."

for i in {1..4}; do
    rm -rf ethereum/node$i/geth/{chaindata,ethash,lightchaindata,nodes,triecache}
    rm -f ethereum/node$i/geth/{LOCK,transactions.rlp}

    # Log file deletion
    LOG_FILE="log/geth_node$i.log"
    if [ -f "$LOG_FILE" ]; then
        > "$LOG_FILE"
        echo "🧾 Cleared $LOG_FILE"
    fi
done

echo "✅ Chain data and logs cleaned. Keystores and configs are safe."