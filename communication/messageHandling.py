
from .message import Message
from .component import Component
from threading import Lock
from threading import Thread
from .component import Action

class MessageHandling():

    def __init__(self):
        self.messages = []
        self.components = dict()
        self._lock = Lock()
        handle_message = Thread(target=self.handle_messages, daemon=True)
        handle_message.start()

    def handle_messages(self):
        while True:
            self._lock.acquire()
            if self.messages:
                message: Message = self.get_first_message()
                self.send_message(message)
            self._lock.release()

    def add_message(self, message: Message):
        self._lock.acquire()
        print(f"event '{message.get_action()}' was added")
        self.messages.append(message)
        self._lock.release()

    def get_messages(self):
        return self.messages
    
    def get_first_message(self):
        return self.messages.pop()
    
    def send_message(self, message: Message):
        try:
            reciever = self.components[message.get_reciever()]
            if issubclass(reciever.__class__, Action):
                print(f"event '{message.get_action()}' was sent")
                reciever.do_action(message.get_action())
        except:
            print(f"Failed to find component with id: {message.get_reciever()}")

    def add_component(self, component: Component):
        self.components.update({component.get_id(): component.get_instance()})

    def remove_component(self, id):
        self.components.pop(id)




        

    