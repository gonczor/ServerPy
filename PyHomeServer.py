#!/usr/bin/env python3

from Networking import ConnectionHandler
from ReadSetup import get_setup
from Interface import Output


if __name__ == '__main__':
    host, port = get_setup()
    connection = ConnectionHandler.setup_connection_handler(host, port)
    try:
        connection.serve_forever()
    except FileNotFoundError:
        Output.config_error()
    except KeyboardInterrupt:
        print('Ending')
    finally:
        connection.shutdown()
