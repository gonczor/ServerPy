#!/usr/bin/env python3

import sys
import signal
import threading

from tests.test_runner import run as run_tests
from Services.EmbeddedServices import EmbeddedCommunicationService
from Services.NetworkServices import NetworkCommunicationService


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


if 'test' in sys.argv:
    run_tests()
else:
    main = Main()
    main.main()
