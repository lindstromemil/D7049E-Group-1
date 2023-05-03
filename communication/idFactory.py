
from threading import Lock

class IdFactory():
    __instance = None

    # Make it a singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(IdFactory, cls).__new__(cls)
            cls.__instance.__initialized  = False
        else:
            cls.__instance.get_new_id()
        return cls.__instance
    
    def __init__(self):
        if(self.__initialized): return
        self.__initialized = True
        self._lock = Lock()
        self.currentID = 0

    def get_new_id(self):
        self._lock.acquire()
        self.currentID += 1
        self._lock.release()
        return self.currentID