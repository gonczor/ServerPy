import socketserver
from datetime import datetime
from Networking import Errors, OrderFactory
import threading


def setup_connection_handler(host, port):
    return ThreadedTCP((host, port), ConnectionHandler)


class BannedAddresses:
    def __init__(self, address):
        self.address = address
        self.ban_timestamp = datetime.now()


class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    banned_addresses = [BannedAddresses(None)]
    lock = threading.Lock()


class ConnectionHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            self.__authorize_connection__()
            self.__receive_data_from_network__()
            order_factory = OrderFactory.OrderFactory.create_factory(self.data)
            order = order_factory.create_order(self.request)
            order.perform_order()

        except Errors.UnknownOrderError:
            # If we receive wring order we can assume that unauthorized connection is attempted.
            # Therefore connection is being shut down.
            print('Wrong order! Shutting connection down.')
            self.request.close()
            self.__ban_client__()

        except Errors.AuthorizationError:
            self.request.close()

    def __receive_data_from_network__(self):
        self.data = self.request.recv(1024)
        self.data = self.data.decode('utf-8')

    # TODO: extend this, introduce password checking
    def __authorize_connection__(self):
        self.__unban_after_withdrawal_period__()
        if self.__is_banned__():
            raise Errors.AuthorizationError

    def __unban_after_withdrawal_period__(self):
        current_timestamp = datetime.now()
        ThreadedTCP.lock.acquire()
        to_delete = []
        for banned in ThreadedTCP.banned_addresses:
            elapsed = current_timestamp - banned.ban_timestamp
            if elapsed.days >= 1 or elapsed.seconds > 60:
                to_delete.append(banned)

        for td in to_delete:
            ThreadedTCP.banned_addresses.remove(td)
        ThreadedTCP.lock.release()

    def __is_banned__(self):
        banned_addresses = (l.address for l in ThreadedTCP.banned_addresses)
        if self.client_address[0] in banned_addresses:
            return True

    def __ban_client__(self):
        ThreadedTCP.banned_addresses.append(BannedAddresses(self.client_address[0]))
