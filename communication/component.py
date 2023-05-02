

class Component():
    def __init__(self, id, instance):
        self.id = id
        self.instance = instance

    def get_id(self):
        return self.id
    
    def get_instance(self):
        return self.instance
    

# Gets implemented in each class that takes events
class Action():
    def do_action(self, action):
        pass