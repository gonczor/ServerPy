import socketserver
import threading
import ssl
from datetime import datetime, timedelta

import os

from Networking import Errors, OrderFactory
from Networking.BannedAddressesCache import BannedAddressesCache


banned_addresses_tmp = []
banned_addresses = BannedAddressesCache()
lock_ban = threading.Lock()


def setup_connection_handler(host, port):
    return ThreadedTCP((host, port), ConnectionHandler)


class BannedAddresses:
    def __init__(self, address):
        self.address = address
        self.ban_expiry = datetime.now() + timedelta(seconds=60)


class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def get_request(self):
        (socket, address) = socketserver.TCPServer.get_request(self)
        return (ssl.wrap_socket(socket, server_side=True,
                                certfile=os.path.join('/Users/gonczor/Documents/Python/ServerPy', 'Configuration',
                                                      'Certificates', 'server.crt'),
                                keyfile=os.path.join('/Users/gonczor/Documents/Python/ServerPy', 'Configuration',
                                                     'Certificates', 'server.key'),
                                ), address)


class ConnectionHandler(socketserver.BaseRequestHandler):
    global banned_addresses_tmp
    global lock_ban

    def handle(self):
        try:
            self._authorize_connection()
            self._receive_data_from_network()
            order_factory = OrderFactory.OrderFactory.create_factory(self.data)
            order = order_factory.create_order(self.request)
            order.perform_order()

        except Errors.UnknownOrderError:
            # If we receive wring order we can assume that unauthorized connection is attempted.
            # Therefore connection is being shut down.
            print('Wrong order! Shutting connection down.')
            self.request.close()
            self._ban_client()

        except Errors.AuthorizationError:
            self.request.close()

    def _receive_data_from_network(self):
        self.data = self.request.recv(1024)
        self.data = self.data.decode('utf-8')

    # TODO: extend this, introduce password checking, SSL
    def _authorize_connection(self):
        if self._is_banned():
            raise Errors.AuthorizationError

    def _is_banned(self):
        return banned_addresses.contains(self.client_address[0])

    def _ban_client(self):
        banned_addresses.add(self.client_address[0])

