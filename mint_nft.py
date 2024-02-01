import json
from eth_hash.backends.pysha3 import keccak256
from web3 import Web3

# Replace with your own values
infura_url = "https://mainnet.infura.io/v3/7d971d5755d142b49329f02a8bfd5d72"
private_key = "46e2623ed463a8523bbc9aea7c1e732fe9768ae9d1c4b5026fc7196252055a42"
contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
wallet_address = "0x99ECb0aBBa20B98Cf096496841241ed5e8a90883"
tokenId = keccak256(nonce) % maxId

# Connect to the Ethereum node
w3 = Web3(Web3.HTTPProvider(infura_url))

# Load the contract ABI
with open('NFT.abi','r') as f:
	abi = json.load(f)

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)

# Build the transaction
nonce = w3.eth.getTransactionCount(wallet_address)
gas_price = w3.eth.gas_price
gas_limit = 100000  # Adjust the gas limit based on your contract's requirements

transaction = contract.functions.mint(wallet_address, tokenId).buildTransaction({
    'from': wallet_address,
    'gas': gas_limit,
    'gasPrice': gas_price,
    'nonce': nonce,
})

# Sign the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

print(f"Transaction sent. Transaction hash: {transaction_hash.hex()}")
