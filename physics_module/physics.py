import pybullet as p
import pybullet_data
import time
import math
from threading import Lock

from communication.action import Action, CharacterMove, OnPressed, CharacterTurned, ObjectMove
from communication.message import Message
from communication.messageHandling import MessageHandling
from direct.task import Task
from communication.idConverter import IdConverter

from communication.bullet import Bullet

# TODO: List of objects --Done but not used yet
# TODO: Be able to move other objects -- Not done yet


class Physics(Action):
    __instance = None

    # Make it a singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Physics, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if (self.__initialized):
            return
        super().__init__()


    # Creates new object and adds id to dictionaries
    # Only handles sample urdfs from pybullet
    def generateObject(self, universalId, object="cube", pos=[0, 0, 1], orientation=[0, 0, 0], scaling=1, movable=True, player=False, plane=False):
        orientation = p.getQuaternionFromEuler(orientation)
        physicsId = p.loadURDF(object + ".urdf", pos,
                               orientation, globalScaling=scaling)
        self.idConverter.add_ids(physicsId, universalId)
        #self.addNewIds(universalId, physicsId)

        # Ugly hack to get playerid and planeid set
        if player:
            self.playerId = physicsId
        if plane:
            self.planeId = physicsId
        if movable:
            return physicsId

        # Might need to update method to make immovable
        p.changeDynamics(physicsId, -1, mass=0)  # Makes object immovable
        return physicsId

    # Move function, moves character based on its orientation
    # Called every update and checks keys in use.
    def updateVelocityPlayer(self):
        # Setup values, should be moved to setup
        maxVelocity = 3.5
        accelerationForward = 0.01
        accelerationSide = 0.01
        jumpScale = 200

        # Check keyboard inputs to get movement direction
        newDirection = [(-self.keys['a']+self.keys['d']) * accelerationSide,
                        (-self.keys['s']+self.keys['w']) * accelerationForward,
                        0
                        ]

        # Normalize vector so max speed is the same in every direction
        mag = math.sqrt(newDirection[0] ** 2 + newDirection[1] ** 2 + newDirection[2] ** 2)
        if mag > 0:
            newDirection = [newDirection[0] / mag,
                            newDirection[1] / mag, 
                            newDirection[2] / mag]

        # Get current velocity and orientation of the object
        pos, orn = p.getBasePositionAndOrientation(self.playerId)
        currentVelocity, _ = p.getBaseVelocity(self.playerId)
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
        #if len(p.getContactPoints(bodyA=self.playerId, bodyB=self.planeId)) > 0:
        # Ugly check if jump is allowed
        # Works better as long as plane is always flat
        if pos[2] < 0.5:
            movementVector[2] += self.keys['space'] * accelerationForward * jumpScale

        p.resetBaseVelocity(self.playerId, movementVector, [0, 0, 0])


    # Updates veloicty of object to given velocity and orientation
    # If no orientation given, uses current orientation of object
    # Does not account for current velocity
    def updateVelocityObject(self, universalId, velocity, orientation=0, zAngle=0):
        #physicsId = self.universalIdtoPhysicsId.get(universalId)
        physicsId = self.idConverter.get_current_id(universalId)

        if orientation == 0:
             _, orientation = p.getBasePositionAndOrientation(physicsId)

        # Get current velocity and orientation of the object
        _, pitch, yaw = p.getEulerFromQuaternion(orientation)

        # Calculate movement vector
        movementVector = [
            velocity * math.sin(yaw) * math.cos(pitch),
            velocity * math.cos(yaw) * math.cos(pitch),
            velocity * zAngle
            # velocity * math.cos(yaw) * math.cos(pitch),
            # velocity * math.sin(yaw) * math.cos(pitch),
            # velocity * math.sin(pitch)
        ]
        p.resetBaseVelocity(physicsId, movementVector)

    # Moves object to 
    def moveObject(self, universalId, pos, ori=0):
        #physicsId = self.universalIdtoPhysicsId.get(universalId)
        physicsId = self.idConverter.get_current_id(universalId)
        if ori == 0:
            _, ori = p.getBasePositionAndOrientation(physicsId)
        p.resetBasePositionAndOrientation(physicsId, pos, ori)

    # Setup for required parts of the physics client
    # Does not start the simulation only sets it up
    def setup(self, renderId):
        self.idConverter = IdConverter()

        self.collisionList = []
        #self.universalIdtoPhysicsId = {}
        #self.physicsIdtoUniversalId = {}
        # Id to render engine
        self.renderId = renderId
        self.keys = {'a': 0, 'd': 0, 'w': 0, 's': 0, 'space': 0}
        # Starts client. Change between DIRECT or GUI, depending if GUI is needed or not
        self.physicsClient = p.connect(p.GUI)
        p.setGravity(0, 0, -10)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        # Sets how long each step of the simulation should be
        p.setTimeStep(1./60)

        # All generate should be in main
        # Move to main when possible
        self.generateObject(0,"plane", pos=[0, 0, 0], movable=False, plane=True)
        self.generateObject(1, player=True)

        self._movementLock = Lock()
        self._keypressLock = Lock()

    # Rename to step!
    # Takes a step in the simulation and tells render where to move objects
    def start(self, task):
        self.updateVelocityPlayer()
        self._movementLock.acquire()
        self.checkCollisionObjects()
        objectIds = self.idConverter.get_all_current_ids()
        beforePosList = []
        for i in objectIds:
            beforePos, _ = (p.getBasePositionAndOrientation(i[0]))
            beforePosList.append(beforePos)
        p.stepSimulation()
        afterPosList = []
        for i in objectIds:
            afterPos, _ = (p.getBasePositionAndOrientation(i[0]))
            afterPosList.append(afterPos)
        self._movementLock.release()
        for i in range(1,len(objectIds)):
            MessageHandling().add_message(Message("physics engine", self.renderId, ObjectMove(objectIds[i][1],
                beforePosList[i][0]-afterPosList[i][0], beforePosList[i][1]-afterPosList[i][1], beforePosList[i][2]-afterPosList[i][2])))
        return Task.cont
    
    def checkCollisionObjects(self):
        #print("Before:", self.collisionList)
        tempList = []
        for id in self.collisionList:
            if len(p.getContactPoints(id)) > 0:
                print(p.getContactPoints(id))
                p.removeBody(id)
                self.idConverter.delete_current_id(id)
            else:
                tempList.append(id)
        #print("After:",self.collisionList)
        self.collisionList = tempList

    # Function to handle actions from other classes
    def do_action(self, action):
        if isinstance(action, Bullet):
            pos, orientation = (p.getBasePositionAndOrientation(self.playerId))
            pos = list(pos)
            pos[2] = pos[2] + 1.5
            physics_id = self.generateObject(action.id, pos=pos, object="cube_small")
            self.collisionList.append(physics_id)
            self.updateVelocityObject(action.id, 40, (orientation[0], orientation[1], -orientation[2], orientation[3]), action.angle)
        if isinstance(action, OnPressed):
            #print("key pressed: ({0} : {1}) inside physics engine".format(action.key, action.value))
            self._keypressLock.acquire()
            self.keys[action.key] = action.value
            self._keypressLock.release()

        if isinstance(action, CharacterTurned):
            # print(action.orientation)
            self._movementLock.acquire()
            currentVelocity, _ = p.getBaseVelocity(self.playerId)
            pos, orientation = (p.getBasePositionAndOrientation(self.playerId))
            p.resetBasePositionAndOrientation(
                self.playerId, pos, (orientation[0], orientation[1], action.orientationX, action.orientationY))
            p.resetBaseVelocity(self.playerId, currentVelocity)
            self._movementLock.release()
