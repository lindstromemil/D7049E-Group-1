
from .idFactory import IdFactory    

# Gets implemented in each class that takes events
class Action():
    def __init__(self):
        self.id = IdFactory().currentID
    def do_action(self, action):
        pass


# ------------------Events------------------



# Input Manager
class OnPressed():
    def __init__(self, key):
        self.key = key
class OnClick():
    def __init__(self, xcord, ycord, button):
        self.xcord = xcord
        self.ycord = ycord
        self.button = button
class MouseMoved():
    def __init__(self, xcord, ycord):
        self.xcord = xcord
        self.ycord = ycord