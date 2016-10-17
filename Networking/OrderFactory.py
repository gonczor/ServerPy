from abc import abstractmethod

from Networking import Orders, Errors


class OrderFactory:
    @staticmethod
    def create_factory(order):
        if order == 'welcome':
            return WelcomeOrderFactory()
        elif order == 'send_file':
            return SendFileOrderFactory()
        else:
            raise Errors.UnknownOrderError

    @abstractmethod
    def create_order(self, request):
        pass


class WelcomeOrderFactory(OrderFactory):
    def create_order(self, request):
        return Orders.Welcome(request)


class SendFileOrderFactory(OrderFactory):
    def create_order(self, request):
        return Orders.SendFile(request)

