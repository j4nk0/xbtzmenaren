from bitcoin_driver import *
import sys
import psycopg2

txid = sys.argv[1]
db_conn = psycopg2.connect(
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432',
    database='xbtzmenaren'
)
cursor = db_conn.cursor()
cursor.execute('SELECT btc FROM xbtzmenarenapp_address')
db_addresses = [ item for (item,) in cursor ]
raw_tx = conn().getrawtransaction(txid)
tx = conn().decoderawtransaction(raw_tx)
for output in tx['vout']:
    for address in output['scriptPubKey']['addresses']:
        if address in db_addresses:
            cursor.execute("SELECT user_id FROM xbtzmenarenapp_address WHERE btc='{address}'".format(address=address))
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO xbtzmenarenapp_incoming_btc (address, btc, confirmations, txid, user_id) VALUES ('{address}', {btc}, {confirmations}, '{txid}', {user_id})".format(address=address, btc=output['value'], confirmations=0, txid=txid, user_id=user_id))
            cursor.execute("UPDATE xbtzmenarenapp_address SET btc='{new_address}' WHERE btc='{address}'".format(new_address=conn().get_new_address(), address=address))
            db_conn.commit()
cursor.close()
db_conn.close()
