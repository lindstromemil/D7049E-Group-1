
from .action import Action, OnClick, OnPressed, MouseMoved


#This is a test class, remove later or use as a frame of reference
class Bullet(Action):
    
    def __init__(self, xangle, yangle):
        super().__init__()
        self.xangle = xangle
        self.yangle = yangle


    def do_action(self, action):
        
        if isinstance(action, MouseMoved):
            print("Mouse moved to ({0} : {1}) inside bullet!".format(action.xcord, action.ycord))

        elif isinstance(action, OnPressed):
            print('key {0} pressed inside bullet!'.format(action.key))
        
        elif isinstance(action, OnClick):
            print("{0} clicked at ({1} : {2}) inside bullet!".format(action.button, action.xcord, action.ycord))

        else:
            print(f"event '{action}' was done in bullet!")