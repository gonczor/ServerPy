import unittest
import socket
import ssl
import os


class BaseTestCase(unittest.TestCase):
    """
    Class provides basic interface for all tests.
    This includes:
      * unwrapped sockets
      * ssl-wrapped sockets
    """
    def __init__(self):
        super(BaseTestCase, self).__init__()
        BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.test_host = '127.0.0.1'
        self.test_port = 12345
        self.ssl_protocol = ssl.PROTOCOL_TLSv1
        self.ciphers = 'ADH-AES256-SHA'
        self.ca_certs_path = os.path.join(BASE_PATH, 'Configuration', 'SSL', 'server.crt')

    def setUp(self):
        super(BaseTestCase, self).setUp()

    def _send_data_via_ssl(self, data, sock=None):
        if not socket:
            sock = self._create_unwrapped_socket()
            sock = self._wrap_socket(sock)

        sock.connect((self.test_host, self.test_port))
        sock.send(data)
        sock.close()

    def _receive_data_via_ssl(self, sock=None, data_size=1024):
        if not sock:
            sock = self._create_unwrapped_socket()
            sock = self._wrap_socket(sock)

        (connection, addr) = sock.accept()
        data = connection.recv(data_size)
        connection.close()
        return data

    @staticmethod
    def _create_unwrapped_socket():
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _wrap_socket(self, s):
        return ssl.wrap_socket(s,
                               ca_certs=self.ca_certs_path,
                               cert_reqs=ssl.CERT_REQUIRED)
