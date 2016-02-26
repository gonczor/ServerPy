#!/usr/bin/env python3

from Interface import Output
from Networking import ConnectionHandler
from Setup.ReadSetup import get_setup
import threading
import signal


class Threads(threading.Thread):
    def __init__(self, service):
        threading.Thread.__init__(self)
        self.service = service

    def run(self):
        self.service.service_entry_point()


class Services:
    # Entry point for threads
    def service_entry_point(self):
        pass


class ClientCommunicationService(Services):
    def __init__(self):
        host, port = get_setup()
        self.__connection__ = ConnectionHandler.setup_connection_handler(host, port)

    def service_entry_point(self):
        try:
            self.__connect__()
        except FileNotFoundError:
            Output.config_error()
        except KeyboardInterrupt:
            print('Ending')
        finally:
            self.__connection__.shutdown()

    # Function will be edited in final version so that restarting server will not be necessary.
    # Currently easier version is used.
    def __connect__(self):
            self.__connection__.serve_forever()

    @staticmethod
    def print_test():
        print('Print test')


class EmbeddedCommunicationService(Services):
    def service_entry_point(self):
        pass


class Main:
    def __init__(self):
        self.client_communication_service = None
        self.embedded_communication_service = None

    def handler(self, signum, frame):
        self.client_communication_service.print_test()

    def main(self):
        signal.signal(signal.SIGHUP, self.handler)

        self.client_communication_service = ClientCommunicationService()
        self.embedded_communication_service = EmbeddedCommunicationService()

        client_communication_service_thread = Threads(self.client_communication_service)
        embedded_communication_service_thread = Threads(self.embedded_communication_service)

        client_communication_service_thread.start()
        embedded_communication_service_thread.start()

        client_communication_service_thread.join()
        embedded_communication_service_thread.join()

if __name__ == '__main__':
    main = Main()
    main.main()
