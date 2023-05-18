from math import pi, sin, cos

from communication.action import Action, OnPressed, CharacterMove, CharacterTurned
from communication.messageHandling import MessageHandling
from communication.message import Message

from physics_module.physics import Physics

from threading import Thread

from communication.bullet import Bullet

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
import sys
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, PerspectiveLens, WindowProperties, LPoint3, LVector3, Point3, NodePath, PandaNode, ClockObject, Quat

class Render(Action, ShowBase):
    __instance = None

    # Make it a singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Render, cls).__new__(cls)
            cls.__instance.__initialized  = False
        return cls.__instance
    
    def __init__(self):
        if(self.__initialized): return
        super().__init__()

    # main setup function called from main
    def setup(self):
        ShowBase.__init__(self)
        self.loadMap("models/environment")
        self.setClock(144)
        self.loadRalph()
        self.setInstructions()
        self.setupInputSettings()
        self.setupCamera()
        self.setupPhysics()
        self.setFullscreen(False)
        self.setVariables()
        self.addTitle("GunAimLab")

        # Start the camera control task:
        self.taskMgr.add(self.controlCamera, "camera-task")

        self.objectRoot = self.render.attachNewNode("objectRoot")
        floor = self.loader.loadModel("render_module/models/npc_1.bam")
        self.createObject(floor,1,"render_module/models/brick-c.jpg",LVector3(0,0,0),10)

    # called upon to close the program
    def close(self, arg):
        self.message_handler.running = False
        sys.exit(arg)

    # long function which defines the behaviour of the camera and ralph sent to the taskmgr as a thread 
    def controlCamera(self, task):
        # figure out how much the mouse has moved (in pixels)
        md = self.win.getPointer(0)

        # send rotation to physics
        angle = -((self.heading % 360)/360) * (pi)
        if self.cursorX != md.getX() or self.cursorY != md.getY():
            xangle = cos(angle) 
            yangle = sin(angle)
            self.message_handler.add_message(Message("render engine", self.physics_id, CharacterTurned(xangle, yangle)))

        self.cursorX = md.getX()
        self.cursorY = md.getY()
        if self.win.movePointer(0, 100, 100):
            self.heading = self.heading - (self.cursorX - 100) * 0.2
            self.pitch = self.pitch - (self.cursorY - 100) * 0.2
        if self.pitch < -45:
            self.pitch = -45
        if self.pitch > 45:
            self.pitch = 45

        self.camera.setHpr(self.heading, self.pitch, 0)
        angle = ((self.heading % 360)/360) * (2*pi)

        dir = self.camera.getMat().getRow3(1)
        self.focus = self.camera.getPos() + (dir * 5)
        self.last = task.time

        self.ralph.setH(self.heading+180)
        self.ralph.setPos(self.ralph.getPos() + LVector3(self.move_x, self.move_y, -self.move_z))
        
        xangle = 1*cos(angle+ pi/2.5) 
        yangle = 1*sin(angle+ pi/2.5)
        self.camera.setPos(self.ralph.getPos() + LVector3(xangle, yangle, 3.5))

        return Task.cont
    
    def loadMap(self, mapPath):
        # Load the environment model.
        self.scene = self.loader.loadModel(mapPath)
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(0, 0, 0)

    # the clock is not actually set here and this code maybe dont do anything
    def setClock(self,framerate):
        # Sets the clockrate/framerate and shows framerate
        self.setFrameRateMeter(True)
        self.clock = ClockObject.get_global_clock()
        self.clock.setMode(ClockObject.MLimited)
        self.clock.setFrameRate(framerate)


    #Loads the model on which the camera is rigged to
    def loadRalph(self):
        ralphStartPos = LVector3(0, 0, 20)
        self.ralph = Actor("render_module/models/ralph")
        self.ralph.reparentTo(render)
        self.ralph.setScale(1)
        self.ralph.setPos(ralphStartPos + (0, 0, 0.5))
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.ralph)
        self.floater.setZ(2.0)

    # adds intructions to be displayed in the game
    def setInstructions(self):
        # Post the instructions
        self.inst1 = self.addInstructions(0.06, "Press ESC to exit")
        self.inst2 = self.addInstructions(0.12, "Move mouse to rotate camera")
        self.inst3 = self.addInstructions(0.18, "W: Move forwards")
        self.inst4 = self.addInstructions(0.24, "S: Move backwards")
        self.inst5 = self.addInstructions(0.30, "A: Move left")
        self.inst6 = self.addInstructions(0.36, "D: Move right")

    #hides mouse and binds keybindings to listeners
    def setupInputSettings(self):
        # Make the mouse invisible, turn off normal mouse controls
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)

        # Setup keyboard controls
        self.keys = {}
        for key in ['a', 'd', 'w', 's', 'space']:
            self.keys[key] = 0
            self.accept(key, self.push_key, [key, 1])
            self.accept('shift-%s' % key, self.push_key, [key, 1])
            self.accept('%s-up' % key, self.push_key, [key, 0])
        self.accept("escape", self.close, [0])
        self.accept('mouse1', self.shootBullet)
        #self.disableMouse()


    def setupCamera(self):
        # Set the current viewing target
        self.focus = LVector3(55, -55, 20)
        self.heading = 180
        self.pitch = 0.0
        self.mousex = 0
        self.mousey = 0
        self.last = 0
        self.mousebtn = [0, 0, 0]

        # Camera settings
        self.lens = PerspectiveLens()
        self.lens.setFov(60)
        self.lens.setNear(0.01)
        self.lens.setFar(1000.0)
        self.cam.node().setLens(self.lens)
        self.heading = -95.0
        self.pitch = 0.0
    
    # sets up message handler and physics so render and physics can communicate
    def setupPhysics(self):
        self.message_handler = MessageHandling()
        self.messagingThread = Thread(target=self.message_handler.handle_messages)
        self.messagingThread.start()

        self.physics_engine = Physics()
        self.physics_engine.setup(self.id)
        self.physics_id = self.physics_engine.id
        self.taskMgr.add(self.physics_engine.start, "physics-start-task")

        self.message_handler.add_component(self.physics_engine)
        self.message_handler.add_component(self.__instance)

    # sets resolution to 1920x1080 if set to True not actually fullscreen
    def setFullscreen(self, bool):
        if bool == True:
            wp = WindowProperties()
            wp.setSize(1920, 1080)
            base.win.requestProperties(wp)

    # Sets various variable used thtoughout render
    def setVariables(self):
        self.move_x = 1
        self.move_y = 1
        self.move_z = 1
        self.cursorX = 100
        self.cursorY = 100

        self.box = 100
        self.universalIdtoRenderId = {}
        self.renderIdtoUniversalId = {}

    def createObject(self, model, UID, texturePath=0, lvector3=LVector3(0,0,0), size=1):
        model.reparentTo(self.objectRoot)
        model.setScale(size)
        model.setPos(lvector3)
        if texturePath != 0:
            myTexture = self.loader.loadTexture(texturePath)
            myTexture.setWrapU(myTexture.WM_repeat)
            model.setTexture(myTexture)
        #self.addNewIds(UID,model)



    def close(self, arg):
        self.message_handler.running = False
        sys.exit(arg)


    
    def setEnvironmentModel(self, path):
        # Load the environment model.
        try:
            self.scene = self.loader.loadModel(path)
        except:
            print("Could not load path")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(0, 0, 0)


        

    def addNewIds(self, universalId, renderId):
        self.universalIdtoRenderId.update(universalId, renderId)
        self.renderIdtoUniversalId.update(renderId, universalId)

    # Function to put instructions on the screen.
    def addInstructions(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)
    
    # Function to put title on the screen, Currently not in use but might look good when done and we have a good name
    def addTitle(self, text):
        return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.08,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))
    
    # simple function used for setting keymaping for WASD & SPACE
    def push_key(self, key, value):
        """Stores a value associated with a key."""
        if self.keys[key] != value:
            self.keys[key] = value
            self.message_handler.add_message(Message("render engine", self.physics_id, OnPressed(key, value)))


    def shootBullet(self):
        xangle = ((self.heading % 360)/360) * (pi)
        yangle = (self.pitch / 360) * (pi)
        bullet = Bullet(xangle, yangle)
        quat = Quat()
        quat.setHpr((self.heading, self.pitch, 0))
        self.message_handler.add_component(bullet)
        self.message_handler.add_message(Message("render engine", self.physics_id, bullet))
        #print(xangle)
        #print(yangle)
        #print("shot bullet")

    def do_action(self, action):
        if isinstance(action, CharacterMove):
            self.move_x = action.xcord*20
            self.move_y = action.ycord*20
            self.move_z = action.zcord*40