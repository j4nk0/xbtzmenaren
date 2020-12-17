from web3 import Web3

provider = Web3.WebsocketProvider('wss://ropsten.infura.io/ws/v3/202896bbe2ad4e428a1fbe4b14a93e99')

w3 = Web3(provider)
print(w3.isConnected())
print(w3.eth.getBlock('latest'))
