import sys
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('localhost', 22554))
socket.send(('NEWBLOCK:' + sys.argv[1] + '*').encode(encoding='UTF-8'))
