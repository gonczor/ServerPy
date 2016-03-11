import os
import time


class Order:
    def __init__(self, request):
        self.request = request

    def get_message(self):
        pass

    def perform_order(self):
        pass

    def __confirm_order__(self):
        self.request.send(self.get_message().encode('utf-8'))


class Welcome(Order):
    def get_message(self):
        return 'welcome\n'

    def perform_order(self):
        self.__confirm_order__()


class SendFile(Order):
    def __init__(self, request):
        super().__init__(request)
        self.__file_size__ = 0
        self.__file_contents__ = None
        self.__file_name__ = 'Test'

    def get_message(self):
        return 'send_file\n'

    def perform_order(self):
        self.__confirm_order__()
        self.__read_file__()
        self.__send_file_size__()
        self.__send_requested_data__()

    def __send_requested_data__(self):
        self.request.sendall(self.__file_contents__)

    def __send_file_size__(self):
        self.request.send(self.__file_size__)
        self.request.send('\n'.encode('utf-8'))
        # TODO temporary solution required to allow client receive file size and content separately
        time.sleep(0.1)

    def __read_file__(self):
        self.__file_size__ = str(os.path.getsize(self.__file_name__)).encode('utf-8')
        f = open(self.__file_name__)
        self.__file_contents__ = f.read().encode('utf-8')
        f.close()
