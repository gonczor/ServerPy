import socket


setup_handler_port = 12346
setup_handler_address = '127.0.0.1'


def setup_handler():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((setup_handler_address, setup_handler_port))
    s.listen(1)

    # Data needs to be transmitted from local host in order to prevent someone from outside
    # modifying the program flow
    data_from_local_host_received = False
    while not data_from_local_host_received:
        conn, addr = s.accept()
        if addr[0] == '127.0.0.1':
            data_from_local_host_received = True


def order_to_shut_down():
    return 'shut_down'
