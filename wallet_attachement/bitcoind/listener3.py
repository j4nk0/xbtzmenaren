import socket
from bitcoin.rpc import RawProxy, JSONRPCError

p = RawProxy()

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
    print('res: ' + res)
    if 'NEWTX' in res:
        txid = res[res.find(':') +1:]
        print('txid: ' + txid)
        p = RawProxy()
        try:
            raw_tx = p.getrawtransaction(txid)
            print('raw_tx: ' + raw_tx)
            tx = p.decoderawtransaction(raw_tx)
            print('tx: ' + str(tx))
            database.append([txid, None, 0])
        except JSONRPCError:
            pass
    elif 'NEWBLOCK' in res:
        blockhash = res[res.find(':') +1:]
        print('blockhash: ' + blockhash)
        p = RawProxy()
        blockdata = p.getblock(blockhash)
        print('blockdata: ' + str(blockdata))
        for row in database:
            try:
                raw_tx = p.getrawtransaction(row[0], False, blockhash)
                print('raw_tx: ' + raw_tx)
                print('confirmations: ' + str(blockdata['confirmations']))
                row[1] = blockhash
                row[2] = blockdata['confirmations']
                tx_detail = p.gettransaction(row[0])
                print('tx_detail: ' + str(tx_detail))
                for output in tx_detail['details']:
                    address = output['address']
                    amount = output['amount']
                    print(' + ', address, ' -> ', amount, ' 0/6')
            except JSONRPCError:
                row[2] = row[1]['confirmations']
                for output in p.gettransaction(row[0])['details']:
                    address = output['address']
                    amount = output['amount']
                    print(' + ', address, ' -> ', amount, ' ', row[2], '/6')


