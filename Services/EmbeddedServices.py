from Embedded.EmbeddedHandler import EmbeddedHandler
from Services.Base import Services


class EmbeddedCommunicationService(Services):
    def __init__(self):
        self._handler = None

    def service_entry_point(self):
        self._handler.serve()

    def _setup(self):
        self._handler = EmbeddedHandler()

    def terminate(self):
        pass

    def reset(self):
        self._handler = EmbeddedHandler()
