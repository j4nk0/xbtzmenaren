import socket
import json
import requests
from decimal import Decimal as D

TRESHOLD_CONFIRMATIONS = 6
CHECK_CONFIRMATIONS = 100

class conn():
    
    url = 'http://localhost:19332/'
    auth = ('ltcrpcuser', 'rpcsecret')
    headers = {'content-type': "application/json", 'cache-control': "no-cache"}

    def getrawtransaction(self, txid):
        payload = json.dumps({"jsonrpc": "1.0", "id":"pythontest", "method": 'getrawtransaction', "params": [txid]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return response.json()['result']

    def is_tx_in_block(self, txid, blockhash):
        payload = json.dumps({"jsonrpc": "1.0", "id":"pythontest", "method": 'getblock', "params": [blockhash, True]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return txid in response.json()['result']['tx']

    def decoderawtransaction(self, raw_tx):
        payload = json.dumps({"method": 'decoderawtransaction', "params": [raw_tx]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return response.json()['result']

    def getblock(self, blockhash):
        payload = json.dumps({"method": 'getblock', "params": [blockhash]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return response.json()['result']
    
    def gettransaction(self, txid):
        payload = json.dumps({"method": 'gettransaction', "params": [txid]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return response.json()['result']

    def getbalance(self):
        payload = json.dumps({"method": 'getbalance', "params": []})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return D(response.json()['result'])

    def get_fee_per_kB(self):
        payload = json.dumps({"method": 'estimatesmartfee', "params": [5]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return D(response.json()['result']['feerate'])

    def send(self, address, amount, fee_per_kB):
        payload = json.dumps({"method": 'settxfee', "params": [str(fee_per_kB)]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        payload = json.dumps({"method": 'sendtoaddress', "params": [address, str(amount)]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)

    def get_new_address(self):
        payload = json.dumps({"method": 'getnewaddress', "params": ['', 'bech32']})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return response.json()['result']

def get_balance():
    return conn().getbalance()

def get_fee_per_kB():
    return conn().get_fee_per_kB()

def send(address, amount, fee_per_kB):
    conn().send(address, amount, fee_per_kB)

def get_new_address():
    return conn().get_new_address()

def get_blockhash(blockhash):
    while True:
        yield blockhash
        blockhash = conn().getblock(blockhash)['previousblockhash']

