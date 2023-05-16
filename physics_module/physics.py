import pybullet as p
import pybullet_data
import time
import math
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
    # Updated version that utilises orientation
    def move(self):
        # Setup values, should be moved to setup
        maxVelocity = 5.0
        minVelocity = -5.0
        accelerationForward = 0.1
        accelerationSide = 0.1
        jumpScale = 20

        # Check keyboard inputs to get movement direction
        newDirection = [(-self.keys['a']+self.keys['d']) * accelerationSide,
                       (-self.keys['s']+self.keys['w']) * accelerationForward,
                       0
                    ]

        # Normalize vector so max speed is the same in every direction
        mag = math.sqrt(newDirection[0] ** 2 + newDirection[1] ** 2 + newDirection[2] ** 2)
        if mag > 0:
            newDirection = [newDirection[0] / mag, newDirection[1] / mag, newDirection[2] / mag]
        
        # Get current velocity and orientation of the object
        pos, orn = p.getBasePositionAndOrientation(self.boxId)
        currentVelocity, _ = p.getBaseVelocity(self.boxId)
        _, _, yaw = p.getEulerFromQuaternion(orn)

        # Calculate movement vector
        movementVector = [
            newDirection[0] * math.cos(yaw) - newDirection[1] * math.sin(yaw),
            newDirection[0] * math.sin(yaw) + newDirection[1] * math.cos(yaw),
            newDirection[2]
        ]

        # Take into account old velocity
        movementVector = [movementVector[i] + currentVelocity[i] for i in range(3)]

        # Calculate actual speed
        movementSpeed = math.sqrt(movementVector[0] ** 2 + movementVector[1] ** 2)
        jump = movementVector[2]
        # If above speed limit adjust speed
        if movementSpeed > maxVelocity:
            movementVector = [movementVector[i] * maxVelocity / movementSpeed for i in range(2)]
            movementVector.append(jump)

        # Checking if jump is allowed, applied after everything else
        if len(p.getContactPoints(bodyA=self.boxId, bodyB=self.planeId)) > 0:
            movementVector[2] += self.keys['space'] * accelerationForward * jumpScale

        p.resetBaseVelocity(self.boxId, movementVector, [0,0,0])





    # Use function to generate
    def setup(self, renderId):
        self.collection = []                                    # List of all objects
        self.renderId = renderId
        self.keys = {'a': 0, 'd': 0, 'w': 0, 's': 0, 'space': 0}
        self.physicsClient = p.connect(p.GUI)
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
            p.resetBasePositionAndOrientation(self.boxId, pos, (orientation[0], orientation[1], action.orientationX, action.orientationY))
            p.resetBaseVelocity(self.boxId, currentVelocity)
            self._lock.release()
