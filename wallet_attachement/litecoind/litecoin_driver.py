import socket
from litecoin_requests import LitecoinRPC
from litecoin_requests.litecoin import JSONRPCError
import json
from .models import Incoming_ltc, Deposit_ltc, Address, Balance
from django.db.models import F
from django.utils import timezone

TRESHOLD_CONFIRMATIONS = 6
CHECK_CONFIRMATIONS = 10
rpc = LitecoinRPC('http://127.0.0.1:19332', 'ltcrpcuser', 'rpcsecret')

def get_balance():
    return rpc.getbalance()

def get_fee_per_kB():
    return rpc.estimatesmartfee(5)['feerate']

def send(address, amount, fee_per_kB):
    rpc.settxfee(fee_per_kB)
    rpc.sendtoaddress(address, amount)

def get_new_address():
    return rpc.getnewaddress('', 'bech32')

def get_blockhash(blockhash):
    while True:
        yield blockhash
        blockhash = rpc.getblock(blockhash)['previousblockhash']

def listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 9331))
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
                raw_tx = rpc.getrawtransaction(txid)
                tx = rpc.decoderawtransaction(raw_tx)
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
                            displayed_address = rpc.getnewaddress('', 'bech32')
                            displayed_address.save()
            except JSONRPCError:
                pass
        elif 'NEWBLOCK' in res:
            new_blockhash = res[res.find(':') +1:]
            for txid in Incoming_ltc.objects.all().values_list('txid', flat=True):
                for (blockhash, _) in zip(get_blockhash(new_blockhash), range(CHECK_CONFIRMATIONS)):
                    try:
                        rpc.getrawtransaction(txid, False, blockhash)
                        confirmations = rpc.getblock(blockhash)['confirmations']
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
                    except JSONRPCError:
                        pass

