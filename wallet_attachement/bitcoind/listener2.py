import socket
from bitcoin.rpc import RawProxy

p = RawProxy()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8331))
serversocket.listen(5)

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
        raw_tx = p.getrawtransaction(txid)
        print('raw_tx: ' + raw_tx)
        tx = p.decoderawtransaction(raw_tx)
        print('tx: ' + str(tx))
