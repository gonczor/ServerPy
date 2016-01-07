#!/usr/bin/env python3

import socketserver
import sys
import Networking
from ReadSetup import get_setup
from Interface import Output


class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ConnectionHandler(socketserver.BaseRequestHandler,):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == '__main__':
    HOST, PORT = get_setup()
    connection = ThreadedTCP((HOST, PORT), ConnectionHandler)
    try:
        connection.serve_forever()
    except FileNotFoundError:
        Output.config_error()
    except KeyboardInterrupt:
        print('Ending')
    finally:
        connection.shutdown()
