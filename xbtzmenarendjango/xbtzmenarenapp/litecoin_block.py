from .models import Incoming_ltc, Deposit_ltc, Address, Balance
from litecoin_driver import *
from django.db.models import F
from django.utils import timezone
import sys

blockhash = sys.argv[1]

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
