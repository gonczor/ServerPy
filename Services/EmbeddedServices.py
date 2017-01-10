from Services.Base import Services


class EmbeddedCommunicationService(Services):
    def __init__(self):
        self._handler = None

    def service_entry_point(self):
        pass

    def _setup(self):
        pass

    def terminate(self):
        pass

    def reset(self):
        pass
