
from threading import Lock

class IdFactory():
    def __init__(self):
        self._lock = Lock()
        self.currentID = 0

    # Make it a singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(IdFactory, cls).__new__(cls)
        return cls.instance

    def get_new_id(self):
        self._lock.acquire()
        self.currentID += 1
        self._lock.release()
        return self.currentID