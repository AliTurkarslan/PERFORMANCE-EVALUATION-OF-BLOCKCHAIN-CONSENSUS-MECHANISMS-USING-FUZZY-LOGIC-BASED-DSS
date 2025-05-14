from web3 import Web3
from solcx import compile_source, install_solc
import json
import os

# Step 1: Install Solidity compiler version
install_solc("0.8.0")

# Step 2: Read contract source code
with open("contracts/kvstore.sol", "r") as f:
    source_code = f.read()

# Step 3: Compile the contract
compiled_sol = compile_source(
    source_code,
    output_values=["abi", "bin"],
    solc_version="0.8.0"
)
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

# Step 4: Connect to local Ethereum node (Node1 - port 8545)
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# Step 5: Define the explicit account address of Node1
from_account = "0x578955Ad5eca98bDf98DA7cFA50e887cc38E07b4"  # Node1 address
w3.eth.default_account = from_account

# Step 6: Connection Check
if not w3.is_connected():
    print("❌ Failed to connect to the Ethereum node.")
    exit(1)

print("🔗 Connected to Ethereum node.")
print(f"📤 Using account: {from_account}")

# Step 7: Deploy the contract
KvStore = w3.eth.contract(abi=abi, bytecode=bytecode)
print("🚀 Sending deployment transaction...")

try:
    tx_hash = KvStore.constructor().transact({
        "from": from_account,
        "gas": 3000000,
        "gasPrice": w3.to_wei(1, "gwei")
    })

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    contract_address = tx_receipt.contractAddress
    print(f"✅ Contract successfully deployed at: {contract_address}")
except Exception as e:
    print(f"❌ Deployment failed: {str(e)}")
    exit(1)

# Step 8: Save ABI and BIN
os.makedirs("build", exist_ok=True)
with open("build/kvstore.abi", "w") as f:
    json.dump(abi, f)
with open("build/kvstore.bin", "w") as f:
    f.write(bytecode)

# Step 9: Save deployed contract address
os.makedirs("log", exist_ok=True)
with open("log/contract_address.txt", "w") as f:
    f.write(contract_address)

print("📦 ABI and contract address saved.")
