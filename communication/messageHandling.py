
from .message import Message
from threading import Lock
from threading import Thread
from .action import Action
from direct.task import Task
#import time

class MessageHandling():
    __instance = None

    # Make it a singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(MessageHandling, cls).__new__(cls)
            cls.__instance.__initialized  = False
        return cls.__instance
    
    def __init__(self):
        if(self.__initialized): return
        self.__initialized = True
        self.messages = []
        self.components = dict()
        self._lock = Lock()
        self.running = True
        # self.handle_message = Thread(target=self.handle_messages, daemon=True)
        # self.handle_message.start()
    
    def handle_messages(self):
        while self.running:
            self._lock.acquire()
            if self.messages:
                print(f"number of events in list: '{len(self.get_messages())}'")
                message: Message = self.get_first_message()
                self.send_message(message)
            self._lock.release()
        #return Task.cont

    def add_message(self, message: Message):
        self._lock.acquire()
        #print(f"event '{message.get_action()}' was added")
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
                #print(f"event '{message.get_action()}' was sent")
                reciever.do_action(message.get_action())
        except KeyError:
            print(f"Failed to find component with id: {message.get_reciever()}")
        except TypeError:
            print("reciever cannot compare to class Action")

    def add_component(self, component: Action):
        if issubclass(component.__class__, Action):
            self.components.update({component.id: component})
        else:
            print("The component does not implement Action Class")
        #self.components.update({component.get_id(): component.get_instance()})

    def remove_component(self, id):
        self.components.pop(id)




        

    