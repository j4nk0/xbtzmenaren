from dogecoin_driver import *
import sys
import psycopg2
from decimal import Decimal as D

blockhash = sys.argv[1]
db_conn = psycopg2.connect(
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432',
    database='xbtzmenaren'
)
cursor = db_conn.cursor()
cursor.execute('SELECT txid FROM xbtzmenarenapp_incoming_doge')
txids = [ item for (item,) in cursor ]
for txid in txids:
    for (blockhash, _) in zip(get_blockhash(blockhash), range(CHECK_CONFIRMATIONS)):
        if conn().is_tx_in_block(txid, blockhash):
            confirmations = conn().getblock(blockhash)['confirmations']
            cursor.execute("UPDATE xbtzmenarenapp_incoming_doge SET confirmations='{confirmations}' WHERE txid='{txid}'".format(confirmations=confirmations, txid=txid))
            db_conn.commit()
            if confirmations >= TRESHOLD_CONFIRMATIONS:
                cursor.execute("SELECT address, doge, user_id FROM xbtzmenarenapp_incoming_doge WHERE txid='{txid}'".format(txid=txid))
                db_conn.commit()
                records = [ record for record in cursor ]
                for record in records:
                    cursor.execute("INSERT INTO xbtzmenarenapp_deposit_doge (address, doge, datetime, user_id) VALUES ('{address}', {doge}, now(), {user_id})".format(address=record[0], doge=record[1], user_id=record[2]))
                    cursor.execute("UPDATE xbtzmenarenapp_balance SET doge = doge + {doge} WHERE user_id={user_id}".format(doge=record[1], user_id=record[2]))
                    db_conn.commit()
                cursor.execute("DELETE FROM xbtzmenarenapp_incoming_doge WHERE txid='{txid}'".format(txid=txid))
                db_conn.commit()
            break
cursor.close()
db_conn.close()
