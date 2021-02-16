import sys
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        my_socket.connect(('localhost', 8331))
        break
    except socket.error:
        pass
my_socket.sendall(('NEWBLOCK:' + sys.argv[1] + '*').encode(encoding='UTF-8'))
my_socket.close()
