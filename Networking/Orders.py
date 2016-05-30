import os
import time


class Order:
    def __init__(self, request):
        self.request = request

    def get_message(self):
        pass

    def perform_order(self):
        pass

    def _confirm_order(self):
        self.request.send(self.get_message().encode('utf-8'))


class Welcome(Order):
    def get_message(self):
        return 'welcome\n'

    def perform_order(self):
        self._confirm_order()


class SendFile(Order):
    def __init__(self, request):
        super().__init__(request)
        self._file_size = 0
        self._file_contents = None
        self._file_name = 'Database/Test'

    def get_message(self):
        return 'send_file\n'

    def perform_order(self):
        self._confirm_order()
        self._send_file_size()
        self._send_requested_data()

    def _send_requested_data(self):
        f = open(self._file_name)
        self.request.sendall(f.read().encode('utf-8'))
        f.close()

    def _send_file_size(self):
        self._file_size = str(os.path.getsize(self._file_name)).encode('utf-8')
        self.request.send(self._file_size)
        self.request.send('\n'.encode('utf-8'))
        # TODO temporary solution required to allow client receive file size and content separately
        time.sleep(0.1)
