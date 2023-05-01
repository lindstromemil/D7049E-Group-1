
from .message import Message
from threading import Lock

class MessageHandling():

    def __init__(self):
        self.messages = []
        self._add_lock = Lock()
        self._handle_lock = Lock()
        self._handle_lock.acquire()

    def handle_messages(self):
        while True:
            self._handle_lock.acquire()
            if self.messages:
                message: Message = self.get_first_message()
                message.do_action()
                self._handle_lock.acquire()

    def add_message(self, message: Message):
        self._add_lock.acquire()
        print("message was added!")
        self.messages.append(message)
        self._handle_lock.release()
        self._add_lock.release()

    def get_messages(self):
        with self._lock:
            return self.messages
    
    def get_first_message(self):
        return self.messages.pop

    