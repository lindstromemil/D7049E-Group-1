from openal import * 
import time

class Sound():
    def __init__(self, folder):
        self.defaultFolder = folder
        self.stop = False


    def play(self, name, volume, x, y):
        while not self.stop:
            source = oalOpen(self.defaultFolder + name)
            source.set_position([x, y, 0])

            listener = Listener()
            listener.set_position([0, 0, 0])
            listener.set_gain(volume)

            source.play()
            #print("Playing at: {0}".format(source.position))

            while source.get_state() == AL_PLAYING:
                time.sleep(1)
        oalQuit()

    def stop(self):
        self.stop = True

    
#Hur man initierar och kallar på den
# soundManager = Sound('Sounds\\')
# soundManager.play('m1garand.wav', 0.1, 0, 0)
