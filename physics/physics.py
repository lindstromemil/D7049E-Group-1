import pybullet as p
import pybullet_data
import time
from threading import Thread

from communication.action import Action, OnPressed
from communication.message import Message
from communication.messageHandling import MessageHandling

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
        self.engine = Thread(target=self.setup, daemon=True)
        self.engine.start()

    def move_right(self):
        p.resetBaseVelocity(self.boxId, [-1, 0, 0])

    def move_left(self):
        #(x, y, z)=p.getBaseVelocity(boxId)
        p.resetBaseVelocity(self.boxId, [1, 1, 4])
        #p.resetBaseVelocity(boxId, (x, y, z + 4))

    def setup(self):
        self.physicsClient = p.connect(p.GUI)
        p.setGravity(0, 0, -10)
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
        self.planeId = p.loadURDF("plane.urdf")
        self.startPos = [0, 0, 1]
        self.startOrientation = p.getQuaternionFromEuler([0, 0, 0])
        self.boxId = p.loadURDF("r2d2.urdf", self.startPos, self.startOrientation)
        self.start()

    
    def start(self):
        for i in range(10000000000000):
            #keys = p.getKeyboardEvents()
            #if ord('d') in keys:
                #self.move_right()
            #if ord('a') in keys:
                #self.move_left()
            p.stepSimulation()
            #object_pos, object_ori = p.getBasePositionAndOrientation(self.boxId)
            #plane_pos, plane_ori = p.getBasePositionAndOrientation(self.planeId)
            #print("Object Position: ", object_pos)
            #print("Object Orientation: ", object_ori)
            #print("Plane Position: ", plane_pos)
            #print("Plane Orientation: ", plane_ori)
            if (i % 240 == 0):
                # boxId = p.loadURDF("r2d2.urdf", startPos, startOrientation)
                pass
            time.sleep(1./240)
        p.disconnect()

    def do_action(self, action):
        if isinstance(action, OnPressed):
            if action.key.char == 'a':
                print('moved left')
                self.move_left()
            elif action.key.char == 'd':
                print('moved right')
                self.move_right()
        #print("did action in engine")



"""
def recieveMessage()
    if instance of move
        resetBaseVelocity ...
    if instance of remove
    if instance of add

def sendMessage(


"""