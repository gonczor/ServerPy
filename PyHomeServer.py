#!/usr/bin/env python3

from Interface import Output
from Networking import ConnectionHandler
from Setup.ReadSetup import get_setup


class Main:
    def __init__(self):
        self.__connection__ = None

    def main(self):
        try:
            self.__connection_thread__()
        except FileNotFoundError:
            Output.config_error()
        except KeyboardInterrupt:
            print('Ending')
        finally:
            self.__connection__.shutdown()

    # Function will be edited in final version so that restarting server will not be necessary.
    # Currently easier version is used.
    def __connection_thread__(self):
            host, port = get_setup()
            self.__connection__ = ConnectionHandler.setup_connection_handler(host, port)
            self.__connection__.serve_forever()

    def __setup_thread__(self):
        pass

    def __SPI_thread(self):
        pass

if __name__ == '__main__':
    main = Main()
    main.main()

