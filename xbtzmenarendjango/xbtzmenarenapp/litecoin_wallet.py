from litecoin_core import *
import sys

txid = sys.argv[1]
raw_tx = conn().getrawtransaction(txid)
tx = conn().decoderawtransaction(raw_tx)
for output in tx['vout']:
    for address in output['scriptPubKey']['addresses']:
        if address in Address.objects.all().values_list('ltc', flat=True):
            #Incoming_ltc.objects.create(
            #    user=Address.objects.get(ltc=address).user,
            #    address=address,
            #    ltc=output['value'],
            #    confirmations=0,
            #    txid=txid
            #)
            #displayed_address = Address.objects.get(ltc=address)
            #displayed_address.ltc = conn().get_new_address()
            #displayed_address.save()

