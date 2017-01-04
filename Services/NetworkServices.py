import time

from Interface import Output
from Networking import ConnectionHandler
from Services.Base import Services
from Setup import Settings


class NetworkCommunicationService(Services):
    def __init__(self):
        self._connection = None
        self._setup()
        self._time_wait = 60

    def _setup(self):
        self._connection = ConnectionHandler.setup_connection_handler(Settings.ADDRESS, Settings.PORT)

    def service_entry_point(self):
        try:
            self._serve()
        except FileNotFoundError:
            Output.config_error()
        finally:
            self._connection.shutdown()

    def _serve(self):
        self._connection.serve_forever()

    def terminate(self):
        self._connection.shutdown()
        self._connection.server_close()
        print('Connection has been shut down.')

    def reset(self):
        self.terminate()
        self._sleep()

    def _sleep(self):
        print('Going to sleep for 60 seconds...')
        t = self._time_wait
        while t > 0:
            time.sleep(5)
            t -= 5
            print('\r{0} seconds remaining...'.format(t), end='')
        print('\nServer restarted.')
