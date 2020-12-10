import socket
import requests
import json

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 22554))
serversocket.listen(5)

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

def get_blockhash(blockhash):
    while True:
        yield blockhash
        blockhash = conn().getblock(blockhash)['previousblockhash']

TRESHOLD_CONFIRMATIONS = 6

database = []

alldata = []
while True:
    (clientsocket, address) = serversocket.accept()
    res = ''
    while True:
        data = clientsocket.recv(5).decode(encoding='UTF-8')
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
            database.append(txid)
            tx = conn().decoderawtransaction(raw_tx)
            for output in tx['vout']:
                for address in output['scriptPubKey']['addresses']:
                    print(' + ', address, ' -> ', output['value'], '0 / 6')
        except:
            raise
            pass
    elif 'NEWBLOCK' in res:
        new_blockhash = res[res.find(':') +1:]
        for row in database:
            for (blockhash, _) in zip(get_blockhash(new_blockhash), range(TRESHOLD_CONFIRMATIONS)):
                if conn().is_tx_in_block(row, blockhash):
                    confirmations = conn().getblock(blockhash)['confirmations']
                    for output in conn().gettransaction(row)['details']:
                        address = output['address']
                        amount = output['amount']
                        print(' + ', address, ' -> ', amount, confirmations, '/ 6')
                    if confirmations == TRESHOLD_CONFIRMATIONS: database.remove(row)
                    break
