import socket
from bitcoin.rpc import RawProxy, JSONRPCError
import json

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8331))
serversocket.listen(5)

def get_blockhash(blockhash):
    while True:
        yield blockhash
        blockhash = RawProxy().getblock(blockhash)['previousblockhash']

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
            raw_tx = RawProxy().getrawtransaction(txid)
            database.append(txid)
            tx = RawProxy().decoderawtransaction(raw_tx)
            for output in tx['vout']:
                for address in output['scriptPubKey']['addresses']:
                    print(' + ', address, ' -> ', output['value'], '0 / 6')
        except JSONRPCError:
            pass
    elif 'NEWBLOCK' in res:
        new_blockhash = res[res.find(':') +1:]
        for row in database:
            for (blockhash, _) in zip(get_blockhash(new_blockhash), range(TRESHOLD_CONFIRMATIONS)):
                try:
                    RawProxy().getrawtransaction(row, False, blockhash)
                    confirmations = RawProxy().getblock(blockhash)['confirmations']
                    for output in RawProxy().gettransaction(row)['details']:
                        address = output['address']
                        amount = output['amount']
                        print(' + ', address, ' -> ', amount, confirmations, '/ 6')
                    if confirmations == TRESHOLD_CONFIRMATIONS: database.remove(row)
                    break
                except JSONRPCError:
                    pass

