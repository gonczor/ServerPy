import socketserver
from datetime import datetime, timedelta

from Networking import Errors, OrderFactory
import threading

banned_addresses = []
lock_ban = threading.Lock()


def setup_connection_handler(host, port):
    return ThreadedTCP((host, port), ConnectionHandler)


class BannedAddresses:
    def __init__(self, address):
        self.address = address
        self.ban_expiry = datetime.now()
        self.ban_expiry += timedelta(seconds=60)


class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ConnectionHandler(socketserver.BaseRequestHandler):
    global banned_addresses
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
        self._unban_after_withdrawal_period()
        if self._is_banned():
            raise Errors.AuthorizationError

    def _unban_after_withdrawal_period(self):
        current_timestamp = datetime.now()
        with lock_ban:
            to_delete = []
            for banned in banned_addresses:
                if self._ban_has_expired(banned, current_timestamp):
                    to_delete.append(banned)

            for td in to_delete:
                banned_addresses.remove(td)

    def _is_banned(self):
        banned = (l.address for l in banned_addresses)
        if self.client_address[0] in banned:
            print("Banned: " + self.client_address[0])
            return True

    def _ban_client(self):
        banned_addresses.append(BannedAddresses(self.client_address[0]))

    @staticmethod
    def _ban_has_expired(banned, current_timestamp):
        return current_timestamp > banned.ban_expiry
