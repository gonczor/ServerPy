from unittest import TestCase

from mock import mock

from Networking.Authentication import AuthenticationHandler
from Networking.Errors import AuthenticationError
from tests.test_utils.NetworkUtils import ConnectionMock


class BannedAddressesMock:
    def __init__(self, addresses_to_add=None):
        self.cache = []
        if addresses_to_add:
            self.cache.append(addresses_to_add)

    def contains(self, key):
        return key in self.cache


class AuthenticationTestCase(TestCase):
    def setUp(self):
        super(AuthenticationTestCase, self).setUp()
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
