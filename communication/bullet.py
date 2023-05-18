
from .action import Action


#This is a test class, remove later or use as a frame of reference
class Bullet(Action):
    
    def __init__(self, angle):
        super().__init__()
        self.angle = angle


    def do_action(self, action):
        if action == "sound":
            print("pew!")
            #TODO fix good sound
            # sound = Sound('audio_module/Sounds\\')
            # soundThread = Thread(target=sound.play,args=('m1garand.wav', 0.1, 0, 0), daemon=True)
            # soundThread.start()