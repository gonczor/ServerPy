import socketserver
from Networking import Errors, OrderFactory, Orders


def setup_connection_handler(host, port):
    return ThreadedTCP((host, port), ConnectionHandler)


class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ConnectionHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.data = None

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

    def __receive_data_from_network__(self):
        self.data = self.request.recv(1024)
        self.data = self.data.decode('utf-8')

    def __authorize_connection__(self):
        pass

