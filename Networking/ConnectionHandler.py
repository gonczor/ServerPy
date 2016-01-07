import socketserver


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
