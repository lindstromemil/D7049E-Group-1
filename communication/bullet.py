
from .action import Action


#This is a test class, remove later or use as a frame of reference
class Bullet(Action):
    def __init__(self):
        super().__init__()

    def do_action(self, action):
        print(f"event '{action}' was done in bullet!")