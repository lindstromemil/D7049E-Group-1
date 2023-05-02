import Ogre
import Ogre.Bites
import Ogre.RTShader
from threading import Thread

from communication.messageHandling import MessageHandling
from communication.component import Event
from communication.message import Message

class KeyListener(Ogre.Bites.InputListener):
    def __init__(self, message_handler: MessageHandling):
        Ogre.Bites.InputListener.__init__(self)
        self.message_handler = message_handler

    def keyPressed(self, evt):
        if evt.keysym.sym == Ogre.Bites.SDLK_ESCAPE:
            event = Event("bullet", "object", "explode")
            message = Message(event)
            self.message_handler.add_message(message)
            #Ogre.Root.getSingleton().queueEndRendering()

        return True

def main():
    ctx = Ogre.Bites.ApplicationContext("PySample")

    ctx.initApp()

    # register for input events

    message_handler = MessageHandling()
    handle_message = Thread(target=message_handler.handle_messages, daemon=True)
    handle_message.start()

    klistener = KeyListener(message_handler) # must keep a reference around
    ctx.addInputListener(klistener)

    root = ctx.getRoot()
    scn_mgr = root.createSceneManager()

    shadergen = Ogre.RTShader.ShaderGenerator.getSingleton()
    shadergen.addSceneManager(scn_mgr)  # must be done before we do anything with the scene

    # without light we would just get a black screen
    scn_mgr.setAmbientLight((.1, .1, .1))

    light = scn_mgr.createLight("MainLight")
    lightnode = scn_mgr.getRootSceneNode().createChildSceneNode()
    lightnode.setPosition(0, 10, 15)
    lightnode.attachObject(light)

    # create the camera
    cam = scn_mgr.createCamera("myCam")
    cam.setNearClipDistance(5)
    cam.setAutoAspectRatio(True)
    camnode = scn_mgr.getRootSceneNode().createChildSceneNode()
    camnode.attachObject(cam)

    # map input events to camera controls
    camman = Ogre.Bites.CameraMan(camnode)
    camman.setStyle(Ogre.Bites.CS_ORBIT)
    camman.setYawPitchDist(0, 0.3, 15)
    ctx.addInputListener(camman)

    # and tell it to render into the main window
    vp = ctx.getRenderWindow().addViewport(cam)
    vp.setBackgroundColour((.3, .3, .3))

    # finally something to render
    ent = scn_mgr.createEntity("Sinbad.mesh")
    node = scn_mgr.getRootSceneNode().createChildSceneNode()
    node.attachObject(ent)

    

    root.startRendering() # blocks until queueEndRendering is called

    ctx.closeApp()

if __name__ == "__main__":
    main()