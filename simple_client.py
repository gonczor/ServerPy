#!/usr/bin/env python3

import socket, ssl, os
BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_sock = ssl.wrap_socket(s,
                           ca_certs=os.path.join(BASE_PATH, 'Configuration', 'SSL', 'server2.crt'),
                           cert_reqs=ssl.CERT_REQUIRED,
                           )

ssl_sock.connect(('192.168.2.193', 12345))

print(ssl_sock.getpeername())
print(ssl_sock.cipher())

# ssl_sock.write()
ssl_sock.send(b'user pass')
received = ssl_sock.recv(1024)
# ssl_sock.write()
data_to_send = input('Give command: ')
ssl_sock.send(bytearray(data_to_send, 'utf-8'))
print('Received: {}'.format(received))

data = ssl_sock.read()

print(data)
