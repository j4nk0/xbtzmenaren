import socket
from litecoin_requests import LitecoinRPC
from litecoin_requests.litecoin import JSONRPCError
import json

rpc = LitecoinRPC('http://127.0.0.1:19332', 'ltcrpcuser', 'rpcsecret')

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 9331))
serversocket.listen(5)

def get_blockhash(blockhash):
    while True:
        yield blockhash
        blockhash = rpc.getblock(blockhash)['previousblockhash']

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
        print('NEWTX', txid)
        try:
            raw_tx = rpc.getrawtransaction(txid)
            database.append(txid)
            tx = rpc.decoderawtransaction(raw_tx)
            for output in tx['vout']:
                for address in output['scriptPubKey']['addresses']:
                    print(' + ', address, ' -> ', output['value'], '0 / 6')
        except JSONRPCError:
            pass
    elif 'NEWBLOCK' in res:
        new_blockhash = res[res.find(':') +1:]
        print('NEWBLOCK', new_blockhash)
        for row in database:
            for (blockhash, _) in zip(get_blockhash(new_blockhash), range(TRESHOLD_CONFIRMATIONS)):
                try:
                    rpc.getrawtransaction(row, False, blockhash)
                    confirmations = rpc.getblock(blockhash)['confirmations']
                    for output in rpc.gettransaction(row)['details']:
                        address = output['address']
                        amount = output['amount']
                        print(' + ', address, ' -> ', amount, confirmations, '/ 6')
                    if confirmations == TRESHOLD_CONFIRMATIONS: database.remove(row)
                    break
                except JSONRPCError:
                    pass
