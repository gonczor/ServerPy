import socketserver
import ssl
from datetime import datetime, timedelta
import os

from . import Errors, OrderFactory
from .Authentication import AuthenticationHandler
from .BannedAddressesCache import BannedAddressesCache
from Setup.settings import BASE_PATH


def setup_connection_handler(host, port):
    return ThreadedTCP((host, port), ConnectionHandler)


class BannedAddresses:
    def __init__(self, address):
        self.address = address
        self.ban_expiry = datetime.now() + timedelta(seconds=60)


class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def get_request(self):
        (socket, address) = socketserver.TCPServer.get_request(self)
        return (ssl.wrap_socket(socket,
                                server_side=True,
                                certfile=os.path.join(BASE_PATH, 'Configuration', 'SSL', 'server.crt'),
                                keyfile=os.path.join(BASE_PATH, 'Configuration', 'SSL', 'server.key'),
                                ssl_version=ssl.PROTOCOL_TLSv1),
                address)


class ConnectionHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.banned_addresses = BannedAddressesCache()

    def handle(self):
        try:
            AuthenticationHandler.authenticate_connection(address=self.client_address[0],
                                                          request=self.request)
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

        except Errors.AuthenticationError:
            self.request.close()

    def _send_certificate(self):
        pass

    def _receive_data_from_network(self):
        self.data = self.request.recv(1024)
        print('Received: {}'.format(self.data))
        self.data = self.data.decode('utf-8')

    def _is_banned(self):
        return self.banned_addresses.contains(self.client_address[0])

    def _ban_client(self):
        self.banned_addresses.add(self.client_address[0])
