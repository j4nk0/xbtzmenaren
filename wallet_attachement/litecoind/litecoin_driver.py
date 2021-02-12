import socket
import json
from .models import Incoming_ltc, Deposit_ltc, Address, Balance
from decimal import Decimal as D
from django.db.models import F
from django.utils import timezone
import requests
import os

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

def listen_for_tx():
    PIPE_PATH = '/run/litecoin_tx'
    os.mkfifo(PIPE_PATH)
    alldata = []
    txids = []
    while True:
        with open(PIPE_PATH) as fifo:
            for line in fifo:
                alldata.append(line)
                if '*' in line:
                    alldata = ''.join(alldata)
                    txids = alldata.split('*')
                    alldata = txids.pop()
                    for txid in txids:
                        raw_tx = conn().getrawtransaction(txid)
                        tx = conn().decoderawtransaction(raw_tx)
                        for output in tx['vout']:
                            for address in output['scriptPubKey']['addresses']:
                                if address in Address.objects.all().values_list('ltc', flat=True):
                                    Incoming_ltc.objects.create(
                                        user=Address.objects.get(ltc=address).user,
                                        address=address,
                                        ltc=output['value'],
                                        confirmations=0,
                                        txid=txid
                                    )
                                    displayed_address = Address.objects.get(ltc=address)
                                    displayed_address.ltc = conn().get_new_address()
                                    displayed_address.save()

def listen_for_block():
    PIPE_PATH = '/run/litecoin_block'
    os.mkfifo(PIPE_PATH)
    alldata = []
    blocks = []
    while True:
        with open(PIPE_PATH) as fifo:
            for line in fifo:
                alldata.append(line)
                if '*' in line:
                    alldata = ''.join(alldata)
                    txids = alldata.split('*')
                    alldata = txids.pop()
                    for new_blockhash in blocks:
                        for txid in Incoming_ltc.objects.all().values_list('txid', flat=True):
                            for (blockhash, _) in zip(get_blockhash(new_blockhash), range(CHECK_CONFIRMATIONS)):
                                if conn().is_tx_in_block(txid, blockhash):
                                    confirmations = conn().getblock(blockhash)['confirmations']
                                    Incoming_ltc.objects.filter(txid=txid).update(confirmations=confirmations)
                                    if confirmations >= TRESHOLD_CONFIRMATIONS:
                                        for record in Incoming_ltc.objects.filter(txid=txid).values('user', 'address', 'ltc'):
                                            Deposit_ltc.objects.create(
                                                address=record['address'],
                                                ltc=record['ltc'],
                                                datetime=timezone.now(),
                                                user_id=record['user']
                                            )
                                            Balance.objects.filter(user=record['user']).update(ltc=F('ltc') + record['ltc'])
                                        Incoming_ltc.objects.filter(txid=txid).delete()
                                    break
