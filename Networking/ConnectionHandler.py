import socketserver


def setup_connection_handler(host, port):
    return ThreadedTCP((host, port), ConnectionHandler)


class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ConnectionHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.data = None

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.__receive_data_from_network__()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
        self.request.close()

    def __receive_data_from_network__(self):
        return self.request.recv(1024)

    def __prepare_order__(self):
        self.data = self.data[1:-1]
