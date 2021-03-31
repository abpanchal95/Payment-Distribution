import json
from web3 import Web3

"""
Ganache is testing blockchain and runs locally.
It can be Downloaded from https://www.trufflesuite.com/ganache
Make sure it is running before executing this code.
"""
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# using first account in ganache as contract owner
owner = web3.eth.accounts[0]
web3.eth.defaultAccount = owner


def deploy_contract(abi, bytecode):
    """Function to deploy contract and returns transaction receipt"""
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    # Get transaction hash of contract creation
    tx_hash = contract.constructor().transact()
    print(f"Contract Block Hash: {web3.toHex(tx_hash)}")

    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt


# loading abi and bytecode json of compiled solidity contract
with open('abi.json', 'r') as f:
    abi = json.loads(f.read())

with open('bytecode.json', 'r') as f:
    bytecode = json.loads(f.read())

# deploying contract and getting contract address
receipt = deploy_contract(abi, bytecode['object'])
contract_address = receipt.contractAddress
print(f"Contract Address: {contract_address}")
contract = web3.eth.contract(address=contract_address, abi=abi)

author_1 = web3.eth.accounts[1]
author_2 = web3.eth.accounts[2]
author_3 = web3.eth.accounts[3]
publisher = web3.eth.accounts[4]
selling_platform_provider = web3.eth.accounts[5]

distibute_to = [
    {"to": author_1, "percent": 6000},  # 60% as 60*100 (solidity doesn't handle float values)
    {"to": author_2, "percent": 1500},
    {"to": author_3, "percent": 1000},
    {"to": publisher, "percent": 1000},
    {"to": selling_platform_provider, "percent": 500},
]

# adding authors, publisher and selling platform provider to contract with their share percentage
for dict_ in distibute_to:
    contract.functions.add(dict_['to'], dict_['percent']).transact()
print("Authors, publisher and selling platform provider added to contract with their share percentage")


print("Customer is Buyin Item")
customer = web3.eth.accounts[6]
tx = {
    "from" : customer,
    "value" : web3.toWei(99, 'ether')  # too costly 😜
}
contract.functions.buy_item().transact(tx)

print("Everyone is having 100 ether in their account")
print("After customer buys item status of everyone's accounts are as below:")
print(f"Customer Account Balance: {web3.fromWei(web3.eth.getBalance(customer), 'ether')}")
print(f"Author 1 Account Balance: {web3.fromWei(web3.eth.getBalance(author_1), 'ether')}")
print(f"Author 2 Account Balance: {web3.fromWei(web3.eth.getBalance(author_2), 'ether')}")
print(f"Author 3 Account Balance: {web3.fromWei(web3.eth.getBalance(author_3), 'ether')}")
print(f"Publisher Account Balance: {web3.fromWei(web3.eth.getBalance(publisher), 'ether')}")
print(f"Selling Platform Provider Account Balance: {web3.fromWei(web3.eth.getBalance(selling_platform_provider), 'ether')}")