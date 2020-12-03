import sys
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('localhost', 9331))
socket.send(('NEWTX:' + sys.argv[1] + '*').encode(encoding='UTF-8'))
