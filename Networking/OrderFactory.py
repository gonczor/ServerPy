from Networking import Orders


class OrderFactory:
    @staticmethod
    def create_factory(order):
        if order == 'welcome':
            return WelcomeOrderFactory()
        elif order == 'send_file':
            return SendFileOrderFactory()
        else:
            raise UnknownOrderError

    def create_order(self):
        pass


class WelcomeOrderFactory(OrderFactory):
    def create_order(self):
        return Orders.Welcome()


class SendFileOrderFactory(OrderFactory):
    def create_order(self):
        return Orders.SendFile()


class UnknownOrderError(Exception):
    pass
