from litecoin_driver import *
from datetime import datetime
import sys

blockhash = sys.argv[1]
db_conn = psycopg2.connect(
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432',
    database='xbtzmenaren'
)
cursor = db_conn.cursor()
cursor.execute('SELECT txid FROM xbtzmenarenapp_incoming_ltc')
txids = [ item for (item,) in cursor ]
for txid in txids:
    for (blockhash, _) in zip(get_blockhash(new_blockhash), range(CHECK_CONFIRMATIONS)):
        if conn().is_tx_in_block(txid, blockhash):
            confirmations = conn().getblock(blockhash)['confirmations']
            cursor.execute("UPDATE xbtzmenarenapp_incoming_ltc SET confirmations='{confirmations}' WHERE txid='{txid}'".format(confirmations=confirmations, txid=txid))
            db_conn.commit()
            if confirmations >= TRESHOLD_CONFIRMATIONS:
                cursor.execute("SELECT address, ltc, user FROM xbtzmenarenapp_incoming_ltc WHERE txid='{txid}'".format(txid=txid))
                for record in cursor:
                    cursor.execute("INSERT INTO xbtzmenarenapp_deposit_ltc (address, ltc, datetime, user_id) VALUES ('{address}', {ltc}, {datetime}, {user_id})".format(address=record[0], ltc=record[1], datetime=datetime.now(), user_id=record[2]))
                    cursor.execute("UPDATE xbtzmenarenapp_balance SET ltc = ltc + {ltc} WHERE user_id={user_id}".format(ltc=record[1], user_id=record[2])) 
                    db_conn.commit() 
                cursor.execute("DELETE FROM xbtzmenarenapp_incoming_ltc WHERE txid='{txid}'".format(txid=txid))
                db_conn.commit()
            break
