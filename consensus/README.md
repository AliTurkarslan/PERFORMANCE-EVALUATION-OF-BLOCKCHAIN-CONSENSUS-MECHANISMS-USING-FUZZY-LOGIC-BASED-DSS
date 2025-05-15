# Consensus-Based Benchmark Modules

This directory contains consensus-specific benchmarking environments for evaluating different Ethereum consensus algorithms under equal conditions. Each subfolder (e.g., `poa`, `pos`, `pow`) contains all the necessary components to set up, run, monitor, and evaluate a 4-node local testnet instance.

---

## Structure Overview

```
consensus/
├── poa/         # Proof of Authority (Clique)
├── pos/         # Proof of Stake (simulated)
├── pow/         # Proof of Work (default Geth mining)
```

Each consensus folder contains the following structure:

```
├── build/       # ABI, bytecode outputs
├── config/      # Configuration and password files
├── contracts/   # Smart contracts to deploy (e.g., kvstore.sol)
├── ethereum/    # Geth node data folders: node1 ... node4
├── genesis/     # Custom genesis block for the network
├── log/         # Deployment and node logs
├── results/     # TPS, latency, energy and gas results
├── scripts/     # Lifecycle, deploy, benchmark, cleanup scripts
```

---

## How It Works (System Lifecycle)

### 1. Setup and Initialization

Each system is designed for full local execution. It begins with node initialization:

```bash
bash scripts/init.sh
```

* Loads `CustomGenesis.json` into each `ethereum/nodeX` directory.
* Genesis files vary by consensus (e.g., Clique config for PoA).

### 2. Start Nodes

```bash
bash scripts/start_all.sh
```

* Starts 4 Geth nodes with proper flags for mining/signing.
* For PoA: Signer addresses must match `extraData` in genesis.
* For PoS: Simulated miner startup is used.

### 3. Deploy Smart Contract

```bash
python3 scripts/deploy_contract.py
```

* Compiles `kvstore.sol`
* Deploys using Web3 on node1 (port 8545)
* Saves ABI, BIN, and contract address for later use

### 4. Transaction Generation

```bash
python3 scripts/generate_transactions.py \
    --tps 100 \
    --duration 60 \
    --scenario poa_100tps \
    --account 0x5789...
```

* Sends key-value writes to smart contract
* Logs each transaction to `tx_log.csv`

### 5. Metric Collection

```bash
python3 scripts/collect_metrics.py --scenario poa_100tps
```

* Waits for confirmations
* Calculates:

  * TPS
  * Latency (avg, p95, variance)
  * Gas usage
  * Block time
  * Simulated energy consumption

### 6. Clean Environment

```bash
bash scripts/clean_all.sh
```

* Clears chaindata and logs (except keystore and genesis)
* Prepares the environment for the next test

---

## Genesis Configuration Notes

Each consensus folder contains its own `CustomGenesis.json`:

* `poa/genesis/CustomGenesis.json`: includes `clique` settings and authorized signers.
* `pos/genesis/CustomGenesis.json`: simplified block sealing.
* `pow/genesis/CustomGenesis.json`: default PoW settings.

---

## Performance Output Files

Each test run creates the following inside `results/{scenario_name}`:

* `metrics_summary.json`: single-file summary of all metrics
* `tx_detailed_log.csv`: per-transaction latency, gas, block

---

## Example Usage (PoA at 500 TPS)

```bash
cd consensus/poa
bash scripts/run_poa_benchmark.sh
```

This script automatically:

* Stops and cleans existing nodes
* Initializes chain
* Starts nodes
* Deploys contract
* Generates and logs 500 TPS for 60 seconds
* Collects performance data

---

## Requirements

* Geth v1.10.26
* Python ≥ 3.8
* Python dependencies: Web3, Pandas, JSON, etc.
* Solidity 0.8.0 (via py-solc-x)

---

## Notes

* Every folder is self-contained: tests can run independently
* Shared account keys must be consistent across all nodes
* Ports and addresses are hardcoded in `scripts/`
* You can extend this to test other consensus (e.g., PBFT)

---

## License

MIT License (see top-level LICENSE file)
