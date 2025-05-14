# Blockchain Consensus Benchmarking Framework + Fuzzy DSS

This repository contains a benchmarking framework to evaluate Ethereum consensus algorithms (PoW, PoA, PoS) using local testnets and a fuzzy logic-based decision support system.

---

## Project Overview

This repository enables the creation of custom Ethereum testnets (each with 4 nodes) to benchmark consensus mechanisms under fixed conditions. It collects performance metrics (TPS, latency, gas, energy), which are then analyzed using a fuzzy inference system to recommend the most suitable consensus algorithm based on user-defined priorities.

---

## 1. Consensus Benchmarking Modules

Each module deploys a separate testnet and executes the same benchmark structure.

### 1.1 Proof of Work (PoW)

* Consensus: mining-based
* Genesis file: `genesis/CustomGenesis_PoW.json`
* Characteristics:

  * High latency
  * Variable block time
  * High energy simulation
* Start:

```bash
bash scripts/run_pow_benchmark.sh
```

### 1.2 Proof of Authority (PoA)

* Consensus: Clique
* Genesis: `genesis/CustomGenesis_PoA.json` (with `extraData` signers)
* Characteristics:

  * Fixed block period (e.g., 5s)
  * Requires signer setup
  * Low energy cost
* Start:

```bash
bash scripts/run_poa_benchmark.sh
```

### 1.3 Proof of Stake (PoS - simulated)

* Simulates PoS behavior for comparison
* Genesis: `genesis/CustomGenesis_PoS.json`
* Uses same scripting as PoW
* Start:

```bash
bash scripts/run_pos_benchmark.sh
```

---

## 2. Scripts and Usage

### 2.1 Blockchain Lifecycle

* `init.sh`: Initializes Geth nodes with custom genesis
* `start_all.sh`: Starts Geth nodes
* `stop_all.sh`: Stops all Geth processes
* `clean_all.sh`: Clears chain data and resets logs

### 2.2 Smart Contract Deployment

* `deploy_contract.py`:

  * Compiles `contracts/kvstore.sol`
  * Deploys it to the current chain
  * Stores deployed address in `log/contract_address.txt`

### 2.3 Transaction Generation

* `generate_transactions.py`:

  * Sends `set()` transactions to the deployed smart contract
  * Controlled by `--tps`, `--duration`, `--scenario`, `--account`
  * Outputs `tx_log.csv`

### 2.4 Metric Collection

* `collect_metrics.py`:

  * Extracts: TPS, latency, block time, energy, gas
  * Outputs:

    * `metrics_summary.json`
    * `tx_detailed_log.csv`

---

## 3. Fuzzy Decision Support System (DSS)

### 3.1 System Architecture

* `define_fuzzy_dss.py`: defines fuzzy logic with 4 performance metrics and 4 priority levels
* `run_inference.py`: computes suitability scores for one priority combo
* `run_batch_inference.py`: iterates all 81 combinations of (low, medium, high) for 4 inputs
* `per_tps_winner_summary.py`: counts how many times each algorithm wins per TPS level
* `plot_tps_winners.py`: visualizes results

### 3.2 Usage

Run all inferences:

```bash
python3 dss/run_batch_inference.py
```

Visualize results:

```bash
python3 dss/plot_tps_winners.py
```

---

## 4. Scenario Configuration

Each consensus is tested under:

* TPS levels: 50, 100, 500
* Duration: 60 seconds
* Smart contract: key-value store
* Output structure:

```
results/
├── pow_50tps/
├── poa_100tps/
├── pos_500tps/
```

---

## 5. Metrics Summary (per scenario)

* `realized_tps`: transactions per second achieved
* `avg_latency`: mean time to mine each tx
* `p95_latency`: 95th percentile latency
* `latency_variance`: variance in tx delay
* `avg_gas_used`: average gas consumption per tx
* `avg_block_time`: mean block interval
* `energy_per_tx`: simulated energy usage per transaction

---

## 6. Example Benchmark Run

```bash
bash scripts/run_pow_benchmark.sh
```

Internally executes:

* `stop_all.sh`
* `clean_all.sh`
* `init.sh`
* `start_all.sh`
* `deploy_contract.py`
* `generate_transactions.py`
* `collect_metrics.py`

---

## 7. Clean Up

```bash
bash scripts/clean_all.sh
```

* Deletes `chaindata`, resets logs
* Preserves keystore/config

---

## 8. Compatibility

* Ethereum client: Geth v1.10.26
* Python: ≥3.8
* Solidity: 0.8.0 via `py-solc-x`
* Libraries:

  * Web3.py
  * scikit-fuzzy
  * matplotlib / seaborn / pandas

---

## 9. Notes

* All benchmarks use the same `kvstore` smart contract
* All testnets use 4 nodes
* Fuzzy DSS supports flexible user priorities
* Designed for reproducibility and modularity

---

## 10. Author

This framework was developed as part of a master's thesis titled:

**Performance Evaluation of Blockchain Consensus Algorithms Using Fuzzy Decision Support Systems**
