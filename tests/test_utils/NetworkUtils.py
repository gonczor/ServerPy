class RequestMock:
    def __init__(self, to_return):
        self.to_return = to_return
        self.to_send = None

    def recv(self, buffer):
        return self.to_return

    def send(self, data):
        self.to_send = data


class ConnectionMock:
    def __init__(self, request_to_return):
        self.request = RequestMock(request_to_return)
        self.address = None
