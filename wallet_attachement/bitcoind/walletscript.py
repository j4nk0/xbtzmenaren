import sys
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        my_socket.connect(('localhost', 8331))
        break
    except:
        pass
my_socket.sendall(('NEWTX:' + sys.argv[1] + '*').encode(encoding='UTF-8'))
my_socket.close()
