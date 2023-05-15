import pybullet as p
import pybullet_data
import time
from threading import Lock

from communication.action import Action, CharacterMove, OnPressed, CharacterTurned
from communication.message import Message
from communication.messageHandling import MessageHandling
from direct.task import Task

# TODO: SET NEW TIMESTEP FOR STEPS (Timestep that fits with render) -- Done
# TODO: Generate objects from function ish done --Done
# TODO: List of objects ish done --Done but not used yet
# TODO: Lookup how to work with urdfs -- Can now scale
# TODO: Be able to move other objects -- Not done yet
# TODO: Make moving dependnt on where rotated -- Done
# TODO: Follow rotation of camera


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


    # Add customPos and orientation as arguments. Make object argurment instead of set to r2d2
    def generateObject(self, object="cube", pos = [0,0,1], orientation = [0, 0, 0], scaling = 1):
        orientation = p.getQuaternionFromEuler(orientation)
        self.boxId = p.loadURDF(object + ".urdf", pos, orientation, globalScaling=scaling)
        self.collection.append(self.boxId)

    # OLD MOVE
    def move2(self):
        #p.resetBaseVelocity(self.boxId, [-self.keys['a']+self.keys['d'], -self.keys['s']+self.keys['w'], 2*self.keys[' ']])

        maxVelocity = 5.0
        minVelocity = -5.0
        accelerationForward = 0.1
        accelerationSide = 0.05
        jumpScale = 50

        currentVelocity, _ = p.getBaseVelocity(self.boxId)

        currentVelocity = list(currentVelocity)

        currentVelocity[0] += (-self.keys['a']+self.keys['d']) * accelerationSide
        currentVelocity[1] += (-self.keys['s']+self.keys['w']) * accelerationForward
        if len(p.getContactPoints(bodyA=self.boxId, bodyB=self.planeId)) > 0:
            currentVelocity[2] += self.keys['space'] * accelerationForward * jumpScale

        #print(p.getContactPoints(bodyA=self.boxId, bodyB=self.planeId))

        for i in range(3):
            if currentVelocity[i] > maxVelocity:
                currentVelocity[i] = maxVelocity
            if currentVelocity[i] < minVelocity:
                currentVelocity[i] = minVelocity



        p.resetBaseVelocity(self.boxId, currentVelocity)

    # Called every update and checks keys in use.
    def move(self):
        maxVelocity = 5.0
        minVelocity = -5.0
        accelerationForward = 0.1
        accelerationSide = 0.1
        jumpScale = 10

        pos, orn = p.getBasePositionAndOrientation(self.boxId)
        rotationMatrix = p.getMatrixFromQuaternion(orn)

        currentVelocity, _ = p.getBaseVelocity(self.boxId)
        currentVelocity = list(currentVelocity)

        newVelocity = [0, 0, 0]

        newVelocity[0] += (-self.keys['a']+self.keys['d']) * accelerationSide
        newVelocity[1] += (-self.keys['s']+self.keys['w']) * accelerationForward

        # Normalize vector so max speed is the same in every direction
        mag = (newVelocity[0] ** 2 + newVelocity[1] ** 2 + newVelocity[2] ** 2) ** 0.5
        if mag > 0:
            newVelocity = [newVelocity[0] / mag, newVelocity[1] / mag, newVelocity[2] / mag]
        
        newVelocity = [currentVelocity[0] + newVelocity [0], currentVelocity[1] + newVelocity [1], currentVelocity[2] + newVelocity [2]]

        if len(p.getContactPoints(bodyA=self.boxId, bodyB=self.planeId)) > 0:
            newVelocity[2] += self.keys['space'] * accelerationForward * jumpScale

        #print(p.getContactPoints(bodyA=self.boxId, bodyB=self.planeId))

        for i in range(2):
            if newVelocity[i] > maxVelocity:
                newVelocity[i] = maxVelocity
            if newVelocity[i] < minVelocity:
                newVelocity[i] = minVelocity

        p.resetBaseVelocity(self.boxId, newVelocity)





    # Use function to generate
    def setup(self, renderId):
        self.collection = []                                    # List of all objects
        self.renderId = renderId
        self.keys = {'a': 0, 'd': 0, 'w': 0, 's': 0, 'space': 0}
        self.physicsClient = p.connect(p.DIRECT)
        p.setGravity(0, 0, -10)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.planeId = p.loadURDF("plane.urdf")
        self.startPos = [0, 0, 1]
        self.startOrientation = p.getQuaternionFromEuler([0, 0, 0])
        self.generateObject(object="cube")
        self._lock = Lock()
        p.setTimeStep(1./144)

    
    def start(self, task):
        self.move()
        self._lock.acquire()
        pos1, _ = (p.getBasePositionAndOrientation(self.boxId))
        p.stepSimulation()
        pos2, _ = (p.getBasePositionAndOrientation(self.boxId))
        self._lock.release()
        MessageHandling().add_message(Message("physics engine", self.renderId, CharacterMove(pos1[0]-pos2[0],pos1[1]-pos2[1],pos1[2]-pos2[2])))
        #MessageHandling().add_message(Message("physics engine", self.renderId, CharacterMove(pos1[0],pos1[1],pos1[2])))

            #object_pos, object_ori = p.getBasePositionAndOrientation(self.boxId)
        return Task.cont

    # def do_action(self, action):
    #     if isinstance(action, OnPressed):
    #         print("key pressed: ({0} : {1}) inside physics engine".format(action.key, action.value))
    #         self.keys[action.key] = action.value

    def do_action(self, action):
        if isinstance(action, OnPressed):
            #print("key pressed: ({0} : {1}) inside physics engine".format(action.key, action.value))
            self.keys[action.key] = action.value

        if isinstance(action, CharacterTurned):
            #print(action.orientation)
            self._lock.acquire()
            currentVelocity, _ = p.getBaseVelocity(self.boxId)
            pos, orientation = (p.getBasePositionAndOrientation(self.boxId))
            #identity_orientation = p.getQuaternionFromEuler([action.orientation,orientation[1],orientation[2]])
            p.resetBasePositionAndOrientation(self.boxId, pos, (orientation[0], orientation[1], action.orientation, 1))
            p.resetBaseVelocity(self.boxId, currentVelocity)
            self._lock.release()
