from bitcoin_driver import *
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
cursor.execute('SELECT txid FROM xbtzmenarenapp_incoming_btc')
txids = [ item for (item,) in cursor ]
for txid in txids:
    for (blockhash, _) in zip(get_blockhash(blockhash), range(CHECK_CONFIRMATIONS)):
        if conn().is_tx_in_block(txid, blockhash):
            confirmations = conn().getblock(blockhash)['confirmations']
            cursor.execute("UPDATE xbtzmenarenapp_incoming_btc SET confirmations='{confirmations}' WHERE txid='{txid}'".format(confirmations=confirmations, txid=txid))
            db_conn.commit()
            if confirmations >= TRESHOLD_CONFIRMATIONS:
                cursor.execute("SELECT address, btc, user_id FROM xbtzmenarenapp_incoming_btc WHERE txid='{txid}'".format(txid=txid))
                db_conn.commit()
                records = [ record for record in cursor ]
                for record in records:
                    cursor.execute("INSERT INTO xbtzmenarenapp_deposit_btc (address, btc, datetime, user_id) VALUES ('{address}', {btc}, now(), {user_id})".format(address=record[0], btc=record[1], user_id=record[2]))
                    cursor.execute("UPDATE xbtzmenarenapp_balance SET btc = btc + {btc} WHERE user_id={user_id}".format(btc=record[1], user_id=record[2])) 
                    db_conn.commit()
                cursor.execute("DELETE FROM xbtzmenarenapp_incoming_btc WHERE txid='{txid}'".format(txid=txid))
                db_conn.commit()
            break
cursor.close()
db_conn.close()
