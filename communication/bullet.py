
from .component import Action


#This is a test class, remove later or use as a frame of reference
class Bullet(Action):

    def do_action(self, action):
        print(f"event '{action}' was done in bullet!")