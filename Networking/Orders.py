class Order:
    def get_message(self):
        raise NotImplementedError('Order must be specified')


class Welcome(Order):
    def get_message(self):
        return 'welcome'


class SendFile(Order):
    def get_message(self):
        return 'send_file'
