import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('localhost', 8331))
socket.send('HELLO_WORLD'.encode(encoding='UTF-8'))
