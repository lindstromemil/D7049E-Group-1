from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
import sys
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, PerspectiveLens, CardMaker, WindowProperties, LPoint3, LVector3, Point3, NodePath, PandaNode

#necessary installation in order to run glb files in panda
#python -m pip install -U panda3d-gltf


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/floor2.glb")
        myTexture = self.loader.loadTexture("models/brick-c.jpg")
        myTexture.setWrapU(myTexture.WM_repeat)
        cm = CardMaker('card')
        card = render.attachNewNode(cm.generate())
        card.setTexture(myTexture)
        self.scene.setTexture(myTexture)

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.scene.setScale(1, 1, 1)
        self.scene.setPos(0, 0, 0)

        ralphStartPos = LVector3(0, 0, -1)
        self.ralph = Actor("models/ralph",
                           {"run": "models/ralph-run",
                            "walk": "models/ralph-walk"})
        self.ralph.reparentTo(render)
        self.ralph.setScale(1)
        self.ralph.setPos(ralphStartPos + (0, 0, 0.5))

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.ralph)
        self.floater.setZ(2.0)

        # Post the instructions
        self.inst1 = addInstructions(0.06, "Press ESC to exit")
        self.inst2 = addInstructions(0.12, "Move mouse to rotate camera")
        self.inst3 = addInstructions(0.18, "W: Move forwards")
        self.inst4 = addInstructions(0.24, "S: Move backwards")
        self.inst5 = addInstructions(0.30, "A: Move left")
        self.inst6 = addInstructions(0.36, "D: Move right")
        


        # Make the mouse invisible, turn off normal mouse controls
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        self.camLens.setFov(60)

        # Setup controls
        self.keys = {}
        for key in ['arrow_left', 'arrow_right', 'arrow_up', 'arrow_down',
                    'a', 'd', 'w', 's']:
            self.keys[key] = 0
            self.accept(key, self.push_key, [key, 1])
            self.accept('shift-%s' % key, self.push_key, [key, 1])
            self.accept('%s-up' % key, self.push_key, [key, 0])
        self.accept('escape', __import__('sys').exit, [0])
        self.disableMouse()

        # Set the current viewing target
        self.focus = LVector3(55, -55, 20)
        self.heading = 180
        self.pitch = 0.0
        self.mousex = 0
        self.mousey = 0
        self.last = 0
        self.mousebtn = [0, 0, 0]

        self.keyMap = {
            "a": 0, "d": 0, "w": 0, "cam-left": 0, "cam-right": 0}
        self.camera.setPos(self.ralph.getX(), self.ralph.getY() + 10, 2)
        self.isMoving = False

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

        def spawnpanda(aX,aY,aZ,bX,bY,bZ):
            # Load and transform the panda actor.
            self.pandaActor = Actor("models/panda-model",
                                    {"walk": "models/panda-walk4"})
            self.pandaActor.setScale(0.005, 0.005, 0.005)
            self.pandaActor.reparentTo(self.render)
            # Loop its animation.
            self.pandaActor.loop("walk")

            # Create the four lerp intervals needed for the panda to
            # walk back and forth.
            posInterval1 = self.pandaActor.posInterval(3,
                                                    Point3(bX, bY, bZ),
                                                    startPos=Point3(aX, aY, aZ))
            posInterval2 = self.pandaActor.posInterval(3,
                                                    Point3(aX, aY, aZ),
                                                    startPos=Point3(bX, bY, bZ))
            hprInterval1 = self.pandaActor.hprInterval(3,
                                                    Point3(180, 0, 0),
                                                    startHpr=Point3(0, 0, 0))
            hprInterval2 = self.pandaActor.hprInterval(3,
                                                    Point3(0, 0, 0),
                                                    startHpr=Point3(180, 0, 0))

            # Create and play the sequence that coordinates the intervals.
            self.pandaPace = Sequence(posInterval1, hprInterval1,
                                    posInterval2, hprInterval2,
                                    name="pandaPace")
            self.pandaPace.loop()

        spawnpanda(15,20,0, 15,-15,0)

        # # Load and transform the panda actor.
        # self.pandaActor = Actor("models/panda-model",
        #                         {"walk": "models/panda-walk4"})
        # self.pandaActor.setScale(0.005, 0.005, 0.005)
        # self.pandaActor.reparentTo(self.render)
        # # Loop its animation.
        # self.pandaActor.loop("walk")

        # # Create the four lerp intervals needed for the panda to
        # # walk back and forth.
        # posInterval1 = self.pandaActor.posInterval(3,
        #                                            Point3(15, -15, 0),
        #                                            startPos=Point3(15, 20, 0))
        # posInterval2 = self.pandaActor.posInterval(3,
        #                                            Point3(15, 20, 0),
        #                                            startPos=Point3(15, -15, 0))
        # hprInterval1 = self.pandaActor.hprInterval(3,
        #                                            Point3(180, 0, 0),
        #                                            startHpr=Point3(0, 0, 0))
        # hprInterval2 = self.pandaActor.hprInterval(3,
        #                                            Point3(0, 0, 0),
        #                                            startHpr=Point3(180, 0, 0))

        # # Create and play the sequence that coordinates the intervals.
        # self.pandaPace = Sequence(posInterval1, hprInterval1,
        #                           posInterval2, hprInterval2,
        #                           name="pandaPace")
        # self.pandaPace.loop()
    
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

        delta = globalClock.getDt()
        move_x = delta * 10 * -self.keys['a'] + delta * 10 * self.keys['d']
        move_z = delta * 10 * self.keys['s'] + delta * 10 * -self.keys['w']
        self.camera.setPos(self.camera, move_x, -move_z, 0)
        self.camera.setHpr(self.heading, self.pitch, 0)

        # startpos = self.ralph.getPos()

        # # If a move-key is pressed, move ralph in the specified direction.

        # if self.keys["a"]:
        #     self.ralph.setH(self.ralph.getH() + 300 * delta)
        # if self.keys["d"]:
        #     self.ralph.setH(self.ralph.getH() - 300 * delta)
        # if self.keys["w"]:
        #     self.ralph.setY(self.ralph, -25 * delta)
        # if self.keys["w"] or self.keys["a"] or self.keys["d"]:
        #     if self.isMoving is False:
        #         self.ralph.loop("run")
        #         self.isMoving = True
        # else:
        #     if self.isMoving:
        #         self.ralph.stop()
        #         self.ralph.pose("walk", 5)
        #         self.isMoving = False

        # # If the camera is too far from ralph, move it closer.
        # # If the camera is too close to ralph, move it farther.

        # camvec = self.ralph.getPos() - self.camera.getPos()
        # camvec.setZ(0)
        # camdist = camvec.length()
        # camvec.normalize()
        # if camdist > 10.0:
        #     self.camera.setPos(self.camera.getPos() + camvec * (camdist - 10))
        #     camdist = 10.0
        # if camdist < 5.0:
        #     self.camera.setPos(self.camera.getPos() - camvec * (5 - camdist))
        #     camdist = 5.0

        # self.camera.lookAt(self.floater)


        return Task.cont
    
    def setMouseBtn(self, btn, value):
        self.mousebtn[btn] = value

    def rotateCam(self, offset):
        self.heading = self.heading - offset * 10

    def push_key(self, key, value):
        """Stores a value associated with a key."""
        self.keys[key] = value

    # Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.08,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))

app = MyApp()
app.run()