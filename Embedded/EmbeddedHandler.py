import time
import datetime

import RPi.GPIO as GPIO

from .lib_nrf24 import NRF24
import spidev


class EmbeddedHandler:
    def __init__(self):
        self.state_check_interval = datetime.timedelta(seconds=10)
        self.state_check_timestamp = datetime.datetime.now()
        GPIO.setmode(GPIO.BCM)

        pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio.begin(0, 17)

        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x76)
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPALevel(NRF24.PA_MIN)

        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()

        self.radio.openWritingPipe(pipes[0])
        self.radio.openReadingPipe(1, pipes[1])
        self.radio.printDetails()

        print('Performing initial pump setup.')
        self._ping(self._to_sendable('SETPUMP00200100'))

    @staticmethod
    def _to_sendable(msg):
        print('To sendable {}'.format(msg))
        msg = list(msg)
        while len(msg) < 32:
            msg.append(0)
        return msg

    def _ping(self, message):
        self.radio.stopListening()
        self.radio.write(message)
        start = time.time()
        self.radio.startListening()
        while not self.radio.available(0):
            if time.time() - start > 2:
                print('Time out')
                return

        received_message = []
        self.radio.read(received_message, self.radio.getDynamicPayloadSize())
        print('Received: {}'.format(received_message))

        print('Translating...')
        string = ''

        for n in received_message:
            if 32 <= n <= 126:
                string += chr(n)
        print('Message decoded to: {}'.format(string))
        self.radio.stopListening()
        
    def serve(self):
        while True:
            if self.state_check_timestamp + self.state_check_interval < datetime.datetime.now():
                self._ping(self._to_sendable('GETSTATE'))
                self.state_check_timestamp = datetime.datetime.now()
