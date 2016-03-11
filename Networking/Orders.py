class Order:
    def get_message(self):
        pass


class Welcome(Order):
    def get_message(self):
        return 'welcome'


class SendFile(Order):
    def get_message(self):
        return 'send_file'
