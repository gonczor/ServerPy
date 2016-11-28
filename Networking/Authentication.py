import threading
from .BannedAddressesCache import BannedAddressesCache
from . import Errors

banned_addresses_tmp = []
banned_addresses = BannedAddressesCache()
lock_ban = threading.Lock()


class AuthenticationHandler:
    """
    Checks whether client has right to connect to the server. Throws proper exceptions if not.
    """
    @staticmethod
    def authenticate_connection(request, address):
        AuthenticationHandler._check_address_is_banned(address)
        AuthenticationHandler._check_correct_credentials_provided(request)
        AuthenticationHandler._send_ack(request)
        print('Connection authorized: {}'.format(address))

    @classmethod
    def _check_address_is_banned(cls, address):
        if banned_addresses.contains(address):
            print('Address: {0} is banned. Access to server denied.'.format(address))
            raise Errors.AuthenticationError

    @classmethod
    def _check_correct_credentials_provided(cls, request):
        data = request.recv(1024)
        username, password = data.split()

        if AuthenticationHandler._get_password(username) != password:
            raise Errors.AuthenticationError

    @classmethod
    def _get_password(cls, username):
        # TODO: implement checking from database
        """
        :return: password required for authentication
        """
        if username == b'user':
            return b'pass'
        else:
            raise Errors.AuthenticationError

    @classmethod
    def _send_ack(cls, request):
        request.send(b'ACK')
