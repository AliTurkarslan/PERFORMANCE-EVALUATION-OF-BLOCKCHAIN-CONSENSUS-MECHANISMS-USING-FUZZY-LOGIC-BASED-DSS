# Blockchain Consensus Benchmarking Framework + Fuzzy DSS

This repository provides a fully automated, reproducible, and extensible benchmarking framework for evaluating Ethereum consensus mechanisms (PoW, PoA, PoS) under controlled conditions. It also includes a Fuzzy Logic-based Decision Support System (DSS) that recommends the most suitable consensus algorithm based on user-defined priorities.

---

## 1. Folder Structure (Standardized Layout)

```
project-root/
├── configs/                            # Common configuration files (optional shared use)
├── consensus/
│   ├── poa/
│   │   ├── build/                      # Contract compilation outputs (ABI, BIN)
│   │   ├── config/                     # Node account passwords
│   │   ├── contracts/                  # Smart contract source: kvstore.sol
│   │   ├── ethereum/                   # Geth data for 4 nodes (node1..node4)
│   │   ├── genesis/                    # Custom genesis.json file
│   │   ├── log/                        # Logs (geth, contract deployment)
│   │   ├── results/                    # Output metrics (e.g., metrics_summary.json)
│   │   └── scripts/                    # All automation scripts (init, start, run...)
│   ├── pos/
│   └── pow/
├── data/                               # Normalized metrics used by DSS
├── dss/                                # Fuzzy decision system codebase
├── results/                            # DSS-level results and analysis
├── scripts/                            # Shared/global utilities (optional)
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## 2. Benchmarking: Consensus Test Environments

Each consensus environment (PoW, PoA, PoS) is tested with:

* A local 4-node Geth network
* Fixed smart contract: `kvstore.sol`
* 3 scenarios per algorithm: 50, 100, 500 TPS
* Identical test duration: 60 seconds

### 2.1 Execution Example (PoA)

```bash
cd consensus/poa
bash scripts/run_poa_benchmark.sh
```

This will:

* Stop and clean previous chain state
* Initialize nodes with `CustomGenesis.json`
* Start nodes and deploy `kvstore.sol`
* Generate transactions at 50, 100, or 500 TPS
* Collect metrics automatically

---

## 3. Smart Contract: kvstore.sol

```solidity
contract KVStore {
    mapping(string => string) store;

    function set(string memory key, string memory value) public {
        store[key] = value;
    }

    function get(string memory key) public view returns (string memory) {
        return store[key];
    }
}
```

* Used for consistent transaction workload across all benchmarks
* Transaction call: `set(key, value)` with dynamic parameters

---

## 4. Metrics Collected (via `collect_metrics.py`)

| Metric             | Description                            |
| ------------------ | -------------------------------------- |
| `realized_tps`     | Transactions per second (achieved)     |
| `avg_latency`      | Mean tx confirmation delay (seconds)   |
| `p95_latency`      | 95th percentile latency                |
| `latency_variance` | Statistical variability in latency     |
| `avg_gas_used`     | Mean gas cost per tx                   |
| `energy_per_tx`    | Estimated energy usage per tx (Joules) |
| `avg_block_time`   | Mean block interval                    |

All results stored in:

```
results/<algorithm>_<tps>tps/
├── metrics_summary.json
├── tx_detailed_log.csv
├── tx_log.csv
```

---

## 5. Fuzzy Decision Support System (DSS)

The DSS module evaluates consensus performance under user-defined preferences. It uses fuzzy logic to model trade-offs and produce a suitability score.

### 5.1 Inputs

* Normalized performance metrics:

  * `latency`, `p95 latency`, `TPS`, `energy`
* User priorities:

  * Each metric can be set to `low`, `medium`, or `high`

### 5.2 Inference Logic

* Defined in `define_fuzzy_dss.py`
* Models rules like: “If TPS is high and TPS priority is high → suitability is high”
* Penalizes low-priority metrics less and rewards high-priority metrics more

### 5.3 Batch Evaluation (All 81 Combinations)

```bash
python3 dss/run_batch_inference.py
```

* Runs fuzzy evaluation for all combinations of user priorities
* Outputs suitability scores for each algorithm × TPS scenario

### 5.4 Outputs

```
results/fuzzy_batch/
├── scores_latency-high_energy-low_tps-high.csv
├── summary_recommendations.csv
├── stacked_bar_tps_wins.png
├── heatmap_tps_wins.png
```

### 5.5 Visualization

```bash
python3 dss/plot_tps_winners.py
```

* Heatmap: Which algorithm wins most often per priority profile
* Stacked Bar: Overall suitability trends by scenario

---

## 6. Environment Cleanup

```bash
bash scripts/clean_all.sh
```

* Deletes node data directories, logs, and resets results for reruns

---

## 7. Requirements

* Geth: v1.10.26 (manually installed)
* Python: ≥ 3.8
* Solidity: 0.8.0 via `py-solc-x`

### Python Packages

Install with:

```bash
pip install -r requirements.txt
```

Key dependencies:

* `web3`, `pandas`, `matplotlib`, `seaborn`, `scikit-fuzzy`

---

## 8. Reproducibility & Extension

* Each consensus module is modular and isolated
* Scenarios are repeatable (same contract, fixed duration)
* DSS logic can be extended (add metrics, change rules)
* Additional consensus modules (e.g., PBFT) can be added under `consensus/`

---

## 9. License

MIT License. See [LICENSE](LICENSE).

---

## 10. Citation

Developed as part of a Master’s Thesis:
**“Performance Evaluation of Blockchain Consensus Algorithms Using Fuzzy Decision Support Systems”**
