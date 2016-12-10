from unittest import TestCase

from mock import mock

from Networking.Authentication import AuthenticationHandler
from Networking.Errors import AuthenticationError


class BannedAddressesMock:
    def __init__(self, addresses_to_add=None):
        self.cache = []
        if addresses_to_add:
            self.cache.append(addresses_to_add)

    def contains(self, key):
        return key in self.cache


class RequestMock:
    def __init__(self, to_return):
        self.to_return = to_return
        self.to_send = None

    def recv(self, buffer):
        return self.to_return

    def send(self, data):
        self.to_send = data


class ConnectionMock:
    def __init__(self, request_to_return):
        self.request = RequestMock(request_to_return)
        self.address = None


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.correct_credentials = b'user pass'
        self.wrong_username_credentials = b'wrong_username pass'
        self.wrong_password_credentials = b'user wrong_pass'
        self.address = '127.0.0.1'
        self.address_to_be_banned = '192.168.0.5'

    @mock.patch('Networking.BannedAddressesCache', BannedAddressesMock)
    def test_authentication_success(self):
        connection = ConnectionMock(self.correct_credentials)
        connection.address = self.address
        AuthenticationHandler.authenticate_connection(connection.request, connection.address)
        self.assertEqual(connection.request.to_send, b'ACK')

    @mock.patch('Networking.BannedAddressesCache', BannedAddressesMock)
    def test_authentication_fail(self):
        with self.assertRaises(AuthenticationError):
            connection = ConnectionMock(self.wrong_password_credentials)
            connection.address = self.address
            AuthenticationHandler.authenticate_connection(connection.request, connection.address)

        with self.assertRaises(AuthenticationError):
            connection = ConnectionMock(self.wrong_username_credentials)
            connection.address = self.address
            AuthenticationHandler.authenticate_connection(connection.request, connection.address)
