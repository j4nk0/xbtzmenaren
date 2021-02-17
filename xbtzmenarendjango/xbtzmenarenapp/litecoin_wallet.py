from litecoin_driver import *
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
cursor.execute('SELECT ltc FROM xbtzmenarenapp_address')
db_addresses = [ item for (item,) in cursor ]
raw_tx = conn().getrawtransaction(txid)
tx = conn().decoderawtransaction(raw_tx)
for output in tx['vout']:
    for address in output['scriptPubKey']['addresses']:
        if address in db_addresses:
            cursor.execute("SELECT user_id FROM xbtzmenarenapp_address WHERE ltc='{address}'".format(address=address))
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO xbtzmenarenapp_incoming_ltc (address, ltc, confirmations, txid, user_id) VALUES ('{address}', {ltc}, {confirmations}, '{txid}', {user_id})".format(address=address, ltc=output['value'], confirmations=0, txid=txid, user_id=user_id))
            cursor.execute("UPDATE xbtzmenarenapp_address SET ltc='{new_address}' WHERE ltc='{address}'".format(new_address=conn().get_new_address(), address=address))
            db_conn.commit()

