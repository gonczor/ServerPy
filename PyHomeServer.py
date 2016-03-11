#!/usr/bin/env python3

from Interface import Output
from Networking import ConnectionHandler
from Setup.ReadSetup import get_setup
import threading
import signal
import time


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

    def reset(self):
        pass


class NetworkCommunicationService(Services):
    def __init__(self):
        self.__connection__ = None
        self.__setup__()
        self.__time_wait__ = 60

    def __setup__(self):
        host, port = get_setup()
        self.__connection__ = ConnectionHandler.setup_connection_handler(host, port)

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

    def reset(self):
        self.terminate()
        self.__sleep__()

    def __sleep__(self):
        print('Going to sleep for 60 seconds...')
        t = self.__time_wait__
        while t > 0:
            time.sleep(5)
            t -= 5
            print('\r{0} seconds remaining...'.format(t), end='')
        print('\nServer restarted.')


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
        self.SIGHUP_flag_raised = False
        self.SIGINT_flag_raised = False

    def stop_server(self, signum, frame):
        self.SIGINT_flag_raised = True
        self.client_communication_service_thread.terminate()

    def reset_server(self, signum, frame):
        self.SIGHUP_flag_raised = True
        self.client_communication_service_thread.reset()

    def main(self):
        while True:
            signal.signal(signal.SIGINT, self.stop_server)
            signal.signal(signal.SIGHUP, self.reset_server)

            self.client_communication_service = NetworkCommunicationService()
            self.embedded_communication_service = EmbeddedCommunicationService()

            self.client_communication_service_thread = Threads(self.client_communication_service)
            self.embedded_communication_service_thread = Threads(self.embedded_communication_service)

            self.client_communication_service_thread.start()
            self.embedded_communication_service_thread.start()

            self.client_communication_service_thread.join()
            self.embedded_communication_service_thread.join()

            if self.SIGINT_flag_raised:
                break
            elif self.SIGHUP_flag_raised:
                self.SIGHUP_flag_raised = False

if __name__ == '__main__':
    main = Main()
    main.main()
