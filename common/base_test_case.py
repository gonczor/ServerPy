import unittest
import socket
import ssl


class BaseTestCase(unittest.TestCase):
    """
    Class provides basic interface for all tests.
    This includes:
      * _send_data_via_ssl - sending data via TCP
    """
    def __init__(self):
        super(BaseTestCase, self).__init__()
        self.test_host = '127.0.0.1'
        self.test_port = 12345
        self.ssl_protocol = ssl.PROTOCOL_TLSv1
        self.ciphers = 'ADH-AES256-SHA'

    def setUp(self):
        super(BaseTestCase, self).setUp()

    def _send_data_via_ssl(self, data, sock=None):
        if not socket:
            sock = self._create_unwraped_socket()
            sock = self._wrap_socket(sock)

        sock.connect((self.test_host, self.test_port))
        sock.send(data)
        sock.close()

    def _receive_data_via_ssl(self, sock=None, data_size=1024):
        if not sock:
            sock = self._create_unwraped_socket()
            sock = self._wrap_socket(sock)

        (connection, addr) = sock.accept()
        data = connection.recv(data_size)
        connection.close()
        return data

    def _create_unwraped_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _wrap_socket(self, s):
        return ssl.wrap_socket(s, ssl_version=self.ssl_protocol, ciphers=self.ciphers)
