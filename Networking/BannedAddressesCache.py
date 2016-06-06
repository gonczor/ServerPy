import threading
from datetime import datetime, timedelta

# Thanks Gareth Rees for useful advice:
# http://codereview.stackexchange.com/questions/128525/server-connection-handler-in-python


class BannedAddressesCache:
    def __init__(self):
        self._lock = threading.Lock()
        self._cache = {}
        self._withdrawal = timedelta(seconds=60)

    def add(self, key):
        """Add host by to the list of banned
        :param key: banned host's IP address
        """
        with self._lock:
            self._cache[key] = datetime.now() + self._withdrawal

    def contains(self, key):
        """Checks whether cache contains host which is banned. Deletes it from banned if the withdrawal is over
        :param key: banned host's IP address
        """
        with self._lock:
            try:
                expiry = self._cache[key]
            except KeyError:
                return False
            if expiry <= datetime.now():
                del self._cache[key]
                return False
            else:
                return True

    def flush(self):
        """Flushes all banned host's whose ban has expired"""
        # TODO: Flushing could be done while server is idle. Consider implementing this
        with self._lock:
            now = datetime.now()
            expired = [key for key, e in self._cache.items() if e <= now]
            for key in expired:
                del self._cache[key]
