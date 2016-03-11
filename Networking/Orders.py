class Order:
    def __init__(self, request):
        self.request = request

    def get_message(self):
        pass

    def perform_order(self):
        pass


class Welcome(Order):
    def __init__(self, request):
        super().__init__(request)

    def get_message(self):
        return 'welcome'

    def perform_order(self):
        self.request.sendall(self.get_message().encode('utf-8'))
        pass


class SendFile(Order):
    def __init__(self, request):
        super().__init__(request)

    def get_message(self):
        return 'send_file'

    def perform_order(self):
        pass
