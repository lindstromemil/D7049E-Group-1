
from .event import Event

class Message():
    def __init__(self, event: Event):
        self.event = event
    
    def get_reciever(self):
        return self.event.receiver
    
    def get_sender(self):
        return self.event.sender
    
    def get_action(self):
        return self.event.action
    
    def do_action(self):
        print(self.get_reciever)
        print(self.get_sender)
        print(self.get_action)