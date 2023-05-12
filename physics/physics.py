import pybullet as p
import pybullet_data
import time
from threading import Thread

from communication.action import Action, CharacterMove, OnPressed
from communication.message import Message
from communication.messageHandling import MessageHandling
from direct.task import Task

# TODO: SET NEW TIMESTEP FOR STEPS
# TODO: Generate objects from function
# TODO: List of objects
# TODO: Clean up code
# TODO: Lookup how to work with urdfs
# TODO: Timestep that fits with render
# TODO: Make non jumpable when in air


class Physics(Action):
    __instance = None

    # Make it a singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Physics, cls).__new__(cls)
            cls.__instance.__initialized  = False
        return cls.__instance
    
    def __init__(self):
        if(self.__initialized): return
        super().__init__()
        # self.engine = Thread(target=self.setup, daemon=True)
        # self.engine.start()


    # Add customPos and orientation as arguments. Make object argurment instead of set to r2d2
    def generateObject(self, object="r2d2"):
        self.startPos = [0, 0, 1]
        self.startOrientation = p.getQuaternionFromEuler([0, 0, 0])
        self.boxId = p.loadURDF("cube.urdf", self.startPos, self.startOrientation)
        self.collection.append(self.boxId)

    def move(self):
        #p.resetBaseVelocity(self.boxId, [-self.keys['a']+self.keys['d'], -self.keys['s']+self.keys['w'], 2*self.keys[' ']])

        maxVelocity = 5.0
        minVelocity = -5.0
        acceleration = 0.1

        currentVelocity, _ = p.getBaseVelocity(self.boxId)

        currentVelocity = list(currentVelocity)

        currentVelocity[0] += (-self.keys['a']+self.keys['d']) * acceleration
        currentVelocity[1] += (-self.keys['s']+self.keys['w']) * acceleration
        currentVelocity[2] += 4*self.keys['space'] * acceleration

        for i in range(3):
            if currentVelocity[i] > maxVelocity:
                currentVelocity[i] = maxVelocity
            if currentVelocity[i] < minVelocity:
                currentVelocity[i] = minVelocity

        p.resetBaseVelocity(self.boxId, currentVelocity)
        #print(p.getBaseVelocity(self.boxId))


    def setup(self, renderId):
        self.collection = []                                    # List of all objects
        self.renderId = renderId
        self.keys = {'a': 0, 'd': 0, 'w': 0, 's': 0, 'space': 0}
        self.physicsClient = p.connect(p.GUI)
        p.setGravity(0, 0, -20)
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
        self.planeId = p.loadURDF("plane.urdf")
        self.startPos = [0, 0, 1]
        self.startOrientation = p.getQuaternionFromEuler([0, 0, 0])
        self.boxId = p.loadURDF("cube.urdf", self.startPos, self.startOrientation)

        p.setTimeStep(1./240)

    
    def start(self, task):
        self.move()
        pos1, _ = (p.getBasePositionAndOrientation(self.boxId))
        p.stepSimulation()
        pos2, _ = (p.getBasePositionAndOrientation(self.boxId))
        MessageHandling().add_message(Message("physics engine", self.renderId, CharacterMove(pos1[0]-pos2[0],pos1[1]-pos2[1],pos1[2]-pos2[2])))
        #MessageHandling().add_message(Message("physics engine", self.renderId, CharacterMove(pos1[0],pos1[1],pos1[2])))

            #object_pos, object_ori = p.getBasePositionAndOrientation(self.boxId)
            #plane_pos, plane_ori = p.getBasePositionAndOrientation(self.planeId)
            #print("Object Position: ", object_pos)
            #print("Object Orientation: ", object_ori)
            #print("Plane Position: ", plane_pos)
            #print("Plane Orientation: ", plane_ori)
        #if (i % 240 == 0):
            # boxId = p.loadURDF("r2d2.urdf", startPos, startOrientation)
            #pass
        #time.sleep(1./240)
        #p.disconnect()
        return Task.cont

    def do_action(self, action):
        if isinstance(action, OnPressed):
            print("key pressed: ({0} : {1}) inside physics engine".format(action.key, action.value))
            self.keys[action.key] = action.value

        # if isinstance(action, MouseMoved):
        #     print("Mouse moved to ({0} : {1}) inside physics engine".format(action.xcord, action.ycord))

        # elif isinstance(action, OnClick):
        #     print("{0} clicked at ({1} : {2}) inside physics engine".format(action.button, action.xcord, action.ycord))