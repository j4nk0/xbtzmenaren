import socket
from bitcoin.rpc import RawProxy, JSONRPCError

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8331))
serversocket.listen(5)

database = []

alldata = []
while True:
    (clientsocket, address) = serversocket.accept()
    res = ''
    while True:
        data = clientsocket.recv(5).decode(encoding='UTF-8')
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
            raw_tx = RawProxy().getrawtransaction(txid)
            database.append([txid, None, 0])
            tx = RawProxy().decoderawtransaction(raw_tx)
            for output in tx['vout']:
                for address in output['scriptPubKey']['addresses']:
                    print(' + ', address, ' -> ', output['value'], ' ', '0/6')
        except JSONRPCError:
            pass
    elif 'NEWBLOCK' in res:
        blockhash = res[res.find(':') +1:]
        for row in database:
            try:
                RawProxy().getrawtransaction(row[0], False, blockhash)
                row[1] = blockhash
                blockdata = RawProxy().getblock(blockhash)
                row[2] = blockdata['confirmations']
                tx_detail = RawProxy().gettransaction(row[0])
                for output in tx_detail['details']:
                    address = output['address']
                    amount = output['amount']
                    print(' + ', address, ' -> ', amount, ' ', row[2], '/6')
            except JSONRPCError:
                row[2] = RawProxy().getblock(row[1])['confirmations']
                for output in RawProxy().gettransaction(row[0])['details']:
                    address = output['address']
                    amount = output['amount']
                    print(' + ', address, ' -> ', amount, ' ', row[2], '/6')
            if row[2] == 6: database.remove(row)


