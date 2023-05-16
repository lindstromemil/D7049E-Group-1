from math import pi, sin, cos

from communication.action import Action, OnPressed, CharacterMove, CharacterTurned
from communication.messageHandling import MessageHandling
from communication.message import Message

from physics_module.physics import Physics

from threading import Thread

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
import sys
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, PerspectiveLens, CardMaker, WindowProperties, LPoint3, LVector3, Point3, NodePath, PandaNode, ClockObject

#TODO: Map mouse movement to function for it to be handled in physics similarily to how key presses are done currently this might improve movement controls
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
        
    def setup(self):
        ShowBase.__init__(self)
        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)


        # Sets the clockrate/framerate and shows framerate
        self.setFrameRateMeter(True)
        self.clock = ClockObject.get_global_clock()
        self.clock.setMode(ClockObject.MLimited)
        self.clock.setFrameRate(144)

        # Apply scale and position transforms on the model.
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(0, 0, 0)

        ralphStartPos = LVector3(0, 0, 20)
        #self.ralph = Actor("render_module/models/ralph")
        self.ralph = Actor("render_module/models/ralph",
                           {"run": "render_module/models/ralph-run",
                            "walk": "render_module/models/ralph-walk"})
        self.ralph.reparentTo(render)
        self.ralph.setScale(1)
        self.ralph.setPos(ralphStartPos + (0, 0, 0.5))

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.ralph)
        self.floater.setZ(2.0)

        self.isMoving = False

        # Post the instructions
        self.inst1 = self.addInstructions(0.06, "Press ESC to exit")
        self.inst2 = self.addInstructions(0.12, "Move mouse to rotate camera")
        self.inst3 = self.addInstructions(0.18, "W: Move forwards")
        self.inst4 = self.addInstructions(0.24, "S: Move backwards")
        self.inst5 = self.addInstructions(0.30, "A: Move left")
        self.inst6 = self.addInstructions(0.36, "D: Move right")

        # Make the mouse invisible, turn off normal mouse controls
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        self.camLens.setFov(60)

        # Setup controls
        self.keys = {}
        for key in ['a', 'd', 'w', 's', 'space']:
            self.keys[key] = 0
            self.accept(key, self.push_key, [key, 1])
            self.accept('shift-%s' % key, self.push_key, [key, 1])
            self.accept('%s-up' % key, self.push_key, [key, 0])
        self.accept('escape', __import__('sys').exit, [0])
        #self.disableMouse()

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

        self.move_x = 1
        self.move_y = 1
        self.move_z = 1

        # Start the camera control task:
        self.taskMgr.add(self.controlCamera, "camera-task")
        self.accept("escape", sys.exit, [0])

        self.message_handler = MessageHandling()
        self.taskMgr.add(self.message_handler.handle_messages, "messasge-task")
        #self.taskMgr.add(self.message_handler.handle_messages, "message-task")


        self.physics_engine = Physics()
        self.physics_engine.setup(self.id)
        self.physics_id = self.physics_engine.id
        #self.taskMgr.add(self.physics_engine.setup, "physics-setup-task")
        self.taskMgr.add(self.physics_engine.start, "physics-start-task")

        self.message_handler.add_component(self.physics_engine)
        self.message_handler.add_component(self.__instance)

        # wp = WindowProperties()
        # wp.setSize(1920, 1080)
        # base.win.requestProperties(wp)

        self.cursorX = 100
        self.cursorY = 100


    
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

    def controlCamera(self, task):
        # figure out how much the mouse has moved (in pixels)
        box = 100
        md = self.win.getPointer(0)
        # send rotation to physics
        angle = ((self.heading % 360)/360)
        if self.cursorX != md.getX() or self.cursorY != md.getY():
            self.message_handler.add_message(Message("render engine", self.physics_id, CharacterTurned(angle)))

        self.cursorX = md.getX()
        self.cursorY = md.getY()
        if self.win.movePointer(0, 100, 100):
            self.heading = self.heading - (self.cursorX - 100) * 0.2
            #self.message_handler.add_message(Message("render engine", self.physics_id, CharacterTurned(self.heading)))
            #MessageHandling().add_message(Message("render engine", self.physics_id, CharacterTurned(self.heading)))
            self.pitch = self.pitch - (self.cursorY - 100) * 0.2
        if self.pitch < -45:
            self.pitch = -45
        if self.pitch > 45:
            self.pitch = 45

        self.camera.setHpr(self.heading, self.pitch, 0)
        #quat = self.camera.getQuat()
        angle = ((self.heading % 360)/360) * (2*pi)
        #print(angle)

        dir = self.camera.getMat().getRow3(1)
        if self.camera.getX() < -box:
            self.camera.setX(-box)
        if self.camera.getX() > box:
            self.camera.setX(box)
        if self.camera.getY() < -box:
            self.camera.setY(-box)
        if self.camera.getY() > box:
            self.camera.setY(box)
        if self.camera.getZ() < 5.0:
            self.camera.setZ(5)
        # if self.camera.getZ() > 5.0:
        #     self.camera.setZ(5)
        self.focus = self.camera.getPos() + (dir * 5)
        self.last = task.time
        #self.camera.setHpr(self.heading, self.pitch, 0)

        #pos = self.ralph.getPos()
        #if -self.move_y > 0.1:
            #if self.isMoving is False:
                #print("false")
                #self.ralph.loop("run")
                #self.isMoving = True
        #else:
            #if self.isMoving:
                #print("true")
                #self.ralph.stop()
                #self.ralph.pose("walk", 5)
                #self.isMoving = False

        self.ralph.setH(self.heading+180)
        self.ralph.setZ(self.ralph, -self.move_z)
        self.ralph.setY(self.ralph, self.move_y)
        self.ralph.setX(self.ralph, self.move_x)
        
        xangle = 1*cos(angle+ pi/2.5) 
        yangle = 1*sin(angle+ pi/2.5)
        #self.camera.setPos(self.ralph.getPos() + LVector3(2, 0, 6))
        self.camera.setPos(self.ralph.getPos() + LVector3(xangle, yangle, 3.5))


        print(x,y)

        if(x != 100.0 or y != 100.0):
            self.taskMgr.add(self.dum, "dum-task")
        return Task.cont
    
    def dum(self, task):
        self.message_handler.add_message(Message("render engine", self.physics_id, CharacterTurned(self.heading)))
        self.last = task.time

    # Function to put instructions on the screen.
    def addInstructions(self, pos, msg):
        return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)
    
    # Function to put title on the screen.
    def addTitle(self, text):
        return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.08,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))
    
    def push_key(self, key, value):
        """Stores a value associated with a key."""
        self.keys[key] = value
        self.message_handler.add_message(Message("render engine", self.physics_id, OnPressed(key, value)))

    def do_action(self, action):
        # if isinstance(action, MouseMoved):
        #     print("Mouse moved to ({0} : {1}) inside render engine".format(action.xcord, action.ycord))
        #     #self.controlCamera(action.xcord, action.ycord)
        
        if isinstance(action, CharacterMove):
            self.move_x = action.xcord*20
            self.move_y = action.ycord*20
            self.move_z = action.zcord*40
            #print("character moved to ({0} : {1} : {2}) inside render engine".format(action.xcord, action.ycord, action.zcord))