import threading
import socket
import time

class UART_thread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.file_directory="" # directory to file with info

    def run(self):
        print('UART thread')
        # gather info
        # write to file
        time.sleep(10) # refresh info after 10 s


class TCP_IP_thread(threading.Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.function = None
        self.file = None

    def run(self):
        self.function = self.sock.recv()
        self.call_function(self.function)

    def call_function(self, function):
        if function == "send_info":
            self.send_info()
            return
        self.sock.sendall("wrong arg")


    def send_info(self):
        self.file = open("info.txt", "r")
        self.sock.sendall(self.file.read(10))

class Server:
    def __init__(self, address='', port=6001):
        self.sock = socket.socket()
        self.sock.bind((address, port))
        self.conn = None
        self.address = None

    def start_server(self):
        while True:
            self.conn, self.address = self.sock.accept()
            th = TCP_IP_thread(self.conn)
            th.start()
