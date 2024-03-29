import socket
from bitcoin.rpc import RawProxy, JSONRPCError
import json
from .models import Incoming_btc, Deposit_btc, Address, Balance
from django.db.models import F
from django.utils import timezone

TRESHOLD_CONFIRMATIONS = 6
CHECK_CONFIRMATIONS = 10
CONF_PATH = '/home/j4nk0/.bitcoin/bitcoin.conf'

def get_balance():
    return RawProxy(btc_conf_file=CONF_PATH).getbalance()

def get_fee_per_kB():
    return RawProxy(btc_conf_file=CONF_PATH).estimatesmartfee(5)['feerate']

def send(address, amount, fee_per_kB):
    RawProxy(btc_conf_file=CONF_PATH).settxfee(fee_per_kB)
    RawProxy(btc_conf_file=CONF_PATH).sendtoaddtess(address, amount)

def get_new_address():
    return RawProxy(btc_conf_file=CONF_PATH).getnewaddress('', 'bech32')

def get_blockhash(blockhash):
    while True:
        yield blockhash
        blockhash = RawProxy(btc_conf_file=CONF_PATH).getblock(blockhash)['previousblockhash']

def listen():
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
            txid = res[res.find(':') +1:]
            try:
                raw_tx = RawProxy(btc_conf_file=CONF_PATH).getrawtransaction(txid)
                tx = RawProxy(btc_conf_file=CONF_PATH).decoderawtransaction(raw_tx)
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
                            displayed_address = Address.objects.get(btc=address)
                            displayed_address.btc = RawProxy(btc_conf_file=CONF_PATH).getnewaddress('', 'bech32')
                            displayed_address.save()
            except JSONRPCError:
                pass
        elif 'NEWBLOCK' in res:
            new_blockhash = res[res.find(':') +1:]
            for txid in Incoming_btc.objects.all().values_list('txid', flat=True):
                for (blockhash, _) in zip(get_blockhash(new_blockhash), range(CHECK_CONFIRMATIONS)):
                    try:
                        RawProxy(btc_conf_file=CONF_PATH).getrawtransaction(txid, False, blockhash)
                        confirmations = RawProxy(btc_conf_file=CONF_PATH).getblock(blockhash)['confirmations']
                        Incoming_btc.objects.filter(txid=txid).update(confirmations=confirmations)
                        if confirmations >= TRESHOLD_CONFIRMATIONS:
                            for record in Incoming_btc.objects.filter(txid=txid).values('user', 'address', 'btc'):
                                    Deposit_btc.objects.create(
                                        address=record['address'],
                                        btc=record['btc'],
                                        datetime=timezone.now(),
                                        user_id=record['user']
                                    )
                                    Balance.objects.filter(user=record['user']).update(btc=F('btc') + record['btc'])
                            Incoming_btc.objects.filter(txid=txid).delete()
                        break
                    except JSONRPCError:
                        pass

