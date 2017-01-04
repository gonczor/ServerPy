class Services:
    # Entry point for threads
    def service_entry_point(self):
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
