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

    def reset(self):
        self.service.reset()

    def terminate(self):
        self.service.terminate()


class Services:
    # Entry point for threads
    def service_entry_point(self):
        pass

    def terminate(self):
        pass


class NetworkCommunicationService(Services):
    def __init__(self):
        self.__connection__ = None
        self.__setup__()

    def __setup__(self):
        host, port = get_setup()
        self.__connection__ = ConnectionHandler.setup_connection_handler(host, port)
        # self.__connection__.allow_reuse_address = True

    def service_entry_point(self):
        try:
            self.__connect__()
        except FileNotFoundError:
            Output.config_error()
        finally:
            self.__connection__.shutdown()

    def __connect__(self):
            self.__connection__.serve_forever()

    def terminate(self):
        self.__connection__.shutdown()
        self.__connection__.server_close()
        print('Connection has been shut down.')


class EmbeddedCommunicationService(Services):
    def service_entry_point(self):
        pass

    def terminate(self):
        pass

    def reset(self):
        pass


class Main:
    def __init__(self):
        self.client_communication_service = None
        self.embedded_communication_service = None
        self.client_communication_service_thread = None
        self.embedded_communication_service_thread = None

    def stop_server(self, signum, frame):
        self.client_communication_service_thread.terminate()

    def main(self):
        signal.signal(signal.SIGTERM, self.stop_server)

        self.client_communication_service = NetworkCommunicationService()
        self.embedded_communication_service = EmbeddedCommunicationService()

        self.client_communication_service_thread = Threads(self.client_communication_service)
        self.embedded_communication_service_thread = Threads(self.embedded_communication_service)

        self.client_communication_service_thread.start()
        self.embedded_communication_service_thread.start()

        self.client_communication_service_thread.join()
        self.embedded_communication_service_thread.join()

if __name__ == '__main__':
    main = Main()
    main.main()
