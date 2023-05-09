from math import pi, sin, cos

from communication.action import Action, MouseMoved
from communication.messageHandling import MessageHandling
from communication.message import Message

from input_module.inputManager import InputListener
from physics.physics import Physics

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
import sys
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, PerspectiveLens, CardMaker, WindowProperties, LPoint3, LVector3, Point3, NodePath, PandaNode

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
        
    def setup(self, renderInstance):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(0, 0, 0)

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

        # Start the camera control task:
        self.taskMgr.add(self.controlCamera, "camera-task")
        self.accept("escape", sys.exit, [0])

        self.message_handler = MessageHandling()
        self.taskMgr.add(self.message_handler.handle_messages, "messasge-task")
        #self.taskMgr.add(self.message_handler.handle_messages, "message-task")


        self.physics_engine = Physics()
        self.taskMgr.add(self.physics_engine.setup, "physics-setup-task")
        self.taskMgr.add(self.physics_engine.start, "physics-start-task")

        self.message_handler.add_component(self.physics_engine)
        self.message_handler.add_component(renderInstance)


    
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
        md = self.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if self.win.movePointer(0, 100, 100):
            self.heading = self.heading - (x - 100) * 0.2
            self.pitch = self.pitch - (y - 100) * 0.2
        if self.pitch < -45:
            self.pitch = -45
        if self.pitch > 45:
            self.pitch = 45
        self.camera.setHpr(self.heading, self.pitch, 0)
        dir = self.camera.getMat().getRow3(1)
        if self.camera.getX() < -20.0:
            self.camera.setX(-20)
        if self.camera.getX() > 20.0:
            self.camera.setX(20)
        if self.camera.getY() < -20.0:
            self.camera.setY(-20)
        if self.camera.getY() > 20.0:
            self.camera.setY(20)
        if self.camera.getZ() < 5.0:
            self.camera.setZ(5)
        if self.camera.getZ() > 5.0:
            self.camera.setZ(5)
        self.focus = self.camera.getPos() + (dir * 5)
        self.last = task.time

        #delta = globalClock.getDt()
        #move_x = delta * 10 * -self.keys['a'] + delta * 10 * self.keys['d']
        #move_z = delta * 10 * self.keys['s'] + delta * 10 * -self.keys['w']
        #self.camera.setPos(self.camera, move_x, -move_z, 0)
        #self.camera.setHpr(self.heading, self.pitch, 0)

        return Task.cont

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

    def do_action(self, action):
        if isinstance(action, MouseMoved):
            print("Mouse moved to ({0} : {1}) inside render engine".format(action.xcord, action.ycord))
            #self.controlCamera(action.xcord, action.ycord)