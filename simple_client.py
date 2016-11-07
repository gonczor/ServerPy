#!/usr/bin/env python3

import socket, ssl, os
BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_sock = ssl.wrap_socket(s,
                           ca_certs=os.path.join(BASE_PATH, 'Configuration', 'SSL', 'server.crt'),
                           cert_reqs=ssl.CERT_REQUIRED,
                           )

ssl_sock.connect(('127.0.0.1', 12345))

print(ssl_sock.getpeername())
print(ssl_sock.cipher())

ssl_sock.write(b'welcome')
ssl_sock.sendall(b'welcome')

data = ssl_sock.read()

print(data)