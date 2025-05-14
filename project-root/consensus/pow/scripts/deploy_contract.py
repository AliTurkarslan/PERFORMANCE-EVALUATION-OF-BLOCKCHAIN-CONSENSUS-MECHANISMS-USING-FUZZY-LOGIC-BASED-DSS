from web3 import Web3
import json
from solcx import compile_source

# Geth HTTP endpoint
w3 = Web3(Web3.HTTPProvider("http://node:8545"))

# Unlock edilmiş hesap
account = "0xb9D47e33A078E2F7C1dd4fEd465B537682D9d16E"

# Smart contract kaynağını oku
with open("/contracts/kvstore.sol", "r") as f:
    source = f.read()

compiled_sol = compile_source(source, output_values=["abi", "bin"])
contract_id, contract_interface = compiled_sol.popitem()

kvstore = w3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])

# Transaction oluştur
tx_hash = kvstore.constructor().transact({"from": account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract deployed at address: {tx_receipt.contractAddress}")