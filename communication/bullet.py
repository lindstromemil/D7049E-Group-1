
from .action import Action, OnClick, OnPressed, MouseMoved


#This is a test class, remove later or use as a frame of reference
class Bullet(Action):
    __instance = None

    # Make it a singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Bullet, cls).__new__(cls)
            cls.__instance.__initialized  = False
        return cls.__instance
    
    def __init__(self):
        if(self.__initialized): return
        self.__initialized = True
        super().__init__()


    def do_action(self, action):
        
        if isinstance(action, MouseMoved):
            print("Mouse moved to ({0} : {1}) inside bullet!".format(action.xcord, action.ycord))

        elif isinstance(action, OnPressed):
            print('key {0} pressed inside bullet!'.format(action.key))
        
        elif isinstance(action, OnClick):
            print("{0} clicked at ({1} : {2}) inside bullet!".format(action.button, action.xcord, action.ycord))

        else:
            print(f"event '{action}' was done in bullet!")