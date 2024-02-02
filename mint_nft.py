import json
import os
from web3 import Web3
from web3.middleware import geth_poa_middleware, construct_sign_and_send_raw_middleware

infura_url = "https://avalanche-fuji.infura.io/v3/7d971d5755d142b49329f02a8bfd5d72"
private_key = "46e2623ed463a8523bbc9aea7c1e732fe9768ae9d1c4b5026fc7196252055a42"
contract_address = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
wallet_address = "0x99ECb0aBBa20B98Cf096496841241ed5e8a90883"

# Connect to the Ethereum node
w3 = Web3(Web3.HTTPProvider(infura_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

with open('NFT.abi','r') as f:
	abi = json.load(f)

wallet_account = w3.eth.account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(wallet_account))
w3.eth.default_account = wallet_address

contract = w3.eth.contract(address=contract_address, abi=abi)
nonce = os.urandom(32)
maxId = contract.functions.maxId().call()

try:
    output = contract.functions.claim(wallet_address, nonce).transact()
    print(output)
    print("NFT claimed")
except Exception as e:
    print(f"Failed to claim NFT: {str(e)}")
