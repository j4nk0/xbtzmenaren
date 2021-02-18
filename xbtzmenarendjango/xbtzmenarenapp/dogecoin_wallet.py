from dogecoin_driver import *
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
cursor.execute('SELECT doge FROM xbtzmenarenapp_address')
db_addresses = [ item for (item,) in cursor ]
raw_tx = conn().getrawtransaction(txid)
tx = conn().decoderawtransaction(raw_tx)
for output in tx['vout']:
    for address in output['scriptPubKey']['addresses']:
        if address in db_addresses:
            cursor.execute("SELECT user_id FROM xbtzmenarenapp_address WHERE doge='{address}'".format(address=address))
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO xbtzmenarenapp_incoming_doge (address, doge, confirmations, txid, user_id) VALUES ('{address}', {doge}, {confirmations}, '{txid}', {user_id})".format(address=address, doge=output['value'], confirmations=0, txid=txid, user_id=user_id))
            cursor.execute("UPDATE xbtzmenarenapp_address SET doge='{new_address}' WHERE doge='{address}'".format(new_address=conn().get_new_address(), address=address))
            db_conn.commit()
cursor.close()
db_conn.close()
