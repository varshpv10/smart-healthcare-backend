from web3 import Web3
import json

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not w3.is_connected():
    raise Exception("Blockchain not connected")

# Replace with your contract address
contract_address = "0xf2Ed79f94a83006798E0F2F8fc51584d8814c58B"

# Paste your ABI JSON inside triple quotes
contract_abi = json.loads("""
[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_hash",
				"type": "string"
			}
		],
		"name": "storeHash",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "getRecords",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "recordHash",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					}
				],
				"internalType": "struct MedicalRecord.Record[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
""")

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Use first Ganache account
account = w3.eth.accounts[0]

def store_hash(hash_value):
    tx_hash = contract.functions.storeHash(hash_value).transact({'from': account})
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()