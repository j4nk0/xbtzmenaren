import socket
from bitcoin.rpc import RawProxy, JSONRPCError
import json
from .models import Incoming_btc, Address, Balance

TRESHOLD_CONFIRMATIONS = 6
CHECK_CONFIRMATIONS = 10

def get_blockhash(blockhash):
    while True:
        yield blockhash
        blockhash = RawProxy().getblock(blockhash)['previousblockhash']

def listen():
    print('IN BITCOIN_DRIVER')
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8331))
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
            print('IN BITCOIN_DRIVER NEWTX')
            txid = res[res.find(':') +1:]
            try:
                raw_tx = RawProxy().getrawtransaction(txid)
                tx = RawProxy().decoderawtransaction(raw_tx)
                for output in tx['vout']:
                    for address in output['scriptPubKey']['addresses']:
                        if address in Address.objects.all().values_list('btc', flat=True):
                            Incoming_btc.objects.create(
                                user=Address.objects.get(btc=address).user,
                                address=address,
                                btc=output['value'],
                                confirmations=0,
                                txid=txid
                            )
            except JSONRPCError:
                pass
        elif 'NEWBLOCK' in res:
            print('IN BITCOIN_DRIVER NEWBLOCK')
            new_blockhash = res[res.find(':') +1:]
            for txid in Incoming_btc.objects.all().values_list('txid', flat=True):
                for (blockhash, _) in zip(get_blockhash(new_blockhash), range(CHECK_CONFIRMATIONS)):
                    try:
                        RawProxy().getrawtransaction(txid, False, blockhash)
                        confirmations = RawProxy().getblock(blockhash)['confirmations']
                        Incoming_btc.objects.filter(txid=txid).update(confirmations=confirmations)
                        if confirmations >= TRESHOLD_CONFIRMATIONS:
                            users = Incoming_btc.objects.filter(txid=txid).values_list('user', flat=True)
                            for user in users:
                                amounts = Incoming_btc.objects.filter(txid=txid).filter(user=user).values_list('btc', flat=True)
                                for amount in amounts:
                                    Balance.objects.filter(user=user).update(btc=F('btc') + amount)
                            Incomig_btc.objects.filter(txid=txid).delete()
                        break
                    except JSONRPCError:
                        pass

