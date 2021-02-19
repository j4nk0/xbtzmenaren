from bitcoin.rpc import RawProxy, JSONRPCError
import json

TRESHOLD_CONFIRMATIONS = 6
CHECK_CONFIRMATIONS = 100
CONF_PATH = '/home/j4nk0/.bitcoin/bitcoin.conf'

class conn():

    def is_tx_in_block(self, txid, blockhash):
        block = RawProxy(btc_conf_file=CONF_PATH).getblock(blockhash)
        return txid in block['tx']

    def getblock(self, blockhash):
        return RawProxy(btc_conf_file=CONF_PATH).getblock(blockhash)

    def getrawtransaction(self, txid):
        return RawProxy(btc_conf_file=CONF_PATH).getrawtransaction(txid)

    def decoderawtransaction(self, raw_tx):
        return RawProxy(btc_conf_file=CONF_PATH).decoderawtransaction(raw_tx)

    def get_new_address(self):
        return RawProxy(btc_conf_file=CONF_PATH).getnewaddress('', 'bech32')

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


