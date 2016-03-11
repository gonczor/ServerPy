class Order:
    def get_message(self):
        pass

    def perform_order(self):
        pass


class Welcome(Order):
    def get_message(self):
        return 'welcome'

    def perform_order(self):
        pass


class SendFile(Order):
    def get_message(self):
        return 'send_file'

    def perform_order(self):
        pass
