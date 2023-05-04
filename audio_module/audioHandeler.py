from openal import * 
import time
from communication.action import Action

class Sound(Action):
    def __init__(self, folder):
        super().__init__()
        self.defaultFolder = folder


    def play(self, name, volume, x, y):
        source = oalOpen(self.defaultFolder + name)
        source.set_position([x, y, 0])

        listener = Listener()
        listener.set_position([0, 0, 0])
        listener.set_gain(volume)

        source.play()
        print("Playing at: {0}".format(source.position))

        while source.get_state() == AL_PLAYING:
            time.sleep(1)
        oalQuit()

    def do_action(self, action):
        if action == "explode":
            self.play('m1garand.wav', 0.1, 0, 0)
        else:
            print(f"Action was done in Sound with id: {self.id}")

    
#Hur man initierar och kallar på den
# soundManager = Sound('Sounds\\')
# soundManager.play('m1garand.wav', 0.1, 0, 0)
