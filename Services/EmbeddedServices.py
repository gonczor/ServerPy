import RPi.GPIO as GPIO
import spidev
from lib_nrf24 import NRF24

# Note: for development purposes I use dummy version of RPi.GPIO, spidev and lib_nrf24 on my laptop.
#  It doesn't do anything apart from providing interface for development without getting import errors.

from Services.Base import Services


class EmbeddedCommunicationService(Services):
    def service_entry_point(self):
        pass

    def terminate(self):
        pass

    def reset(self):
        pass
