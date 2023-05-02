

class Message():
    def __init__(self, sender, receiever, action):
        self.sender = sender
        self.receiver = receiever
        self.action = action
    
    def get_reciever(self):
        return self.receiver
    
    def get_sender(self):
        return self.sender
    
    def get_action(self):
        return self.action