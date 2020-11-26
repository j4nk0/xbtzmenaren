import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8331))
serversocket.listen(5)

while True:
    (clientsocket, address) = serversocket.accept()
    alldata = []
    while True:
        data = clientsocket.recv(5)
        if not data:
            print(b''.join(alldata))
            break
        alldata.append(data)


