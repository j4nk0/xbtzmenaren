import socket

print('HERE')
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('HERE')
serversocket.bind(('localhost', 8331))
print('HERE')
serversocket.listen(5)

while True:
    (clientsocket, address) = serversocket.accept()
    print(clientsocket.recv(5))
