import socket
import json
from .models import Incoming_doge, Deposit_doge, Address, Balance
from django.db.models import F
from django.utils import timezone
import requests

TRESHOLD_CONFIRMATIONS = 6
CHECK_CONFIRMATIONS = 10

class conn():
    
    url = 'http://localhost:44555/'
    auth = ('rpcuser', 'rpcsecret')
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
        return response.json()['result']

    def get_fee_per_kB(self):
        payload = json.dumps({"method": 'estimatesmartfee', "params": [5]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        return response.json()['result']['feerate']

    def send(self, address, amount, fee_per_kB):
        payload = json.dumps({"method": 'settxfee', "params": [fee_per_kB]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)
        payload = json.dumps({"method": 'sendtoaddress', "params": [address, str(amount)]})
        response = requests.post(url=self.url, auth=self.auth, data=payload, headers=self.headers)

    def get_new_address(self):
        payload = json.dumps({"method": 'getnewaddress', "params": []})
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

def listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 22554))
    serversocket.listen(5)
    alldata = []
    while True:
        (clientsocket, address) = serversocket.accept()
        res = ''
        while True:
            data = clientsocket.recv(1024).decode(encoding='UTF-8')
            if '*' in data:
                alldata.append(data[:data.find('*')])
                res = ''.join(alldata)
                alldata = [data[data.find('*') +1:]]
                break
            else:
                alldata.append(data)
        if 'NEWTX' in res:
            txid = res[res.find(':') +1:]
            try:
                raw_tx = conn().getrawtransaction(txid)
                tx = conn().decoderawtransaction(raw_tx)
                for output in tx['vout']:
                    for address in output['scriptPubKey']['addresses']:
                        if address in Address.objects.all().values_list('doge', flat=True):
                            Incoming_doge.objects.create(
                                user=Address.objects.get(doge=address).user,
                                address=address,
                                doge=output['value'],
                                confirmations=0,
                                txid=txid
                            )
                            displayed_address = Address.objects.get(doge=address)
                            displayed_address.doge = conn().get_new_address()
                            displayed_address.save()
            except:
                raise
                pass
        elif 'NEWBLOCK' in res:
            new_blockhash = res[res.find(':') +1:]
            for txid in Incoming_doge.objects.all().values_list('txid', flat=True):
                for (blockhash, _) in zip(get_blockhash(new_blockhash), range(CHECK_CONFIRMATIONS)):
                    if conn().is_tx_in_block(txid, blockhash):
                        confirmations = conn().getblock(blockhash)['confirmations']
                        Incoming_doge.objects.filter(txid=txid).update(confirmations=confirmations)
                        if confirmations >= TRESHOLD_CONFIRMATIONS:
                            for record in Incoming_doge.objects.filter(txid=txid).values('user', 'address', 'doge'):
                                    Deposit_doge.objects.create(
                                        address=record['address'],
                                        doge=record['doge'],
                                        datetime=timezone.now(),
                                        user_id=record['user']
                                    )
                                    Balance.objects.filter(user=record['user']).update(doge=F('doge') + record['doge'])
                            Incoming_doge.objects.filter(txid=txid).delete()
                        break

