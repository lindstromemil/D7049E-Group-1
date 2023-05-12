import pybullet as p
import pybullet_data
import time
from threading import Thread

from communication.action import Action, CharacterMove, OnPressed
from communication.message import Message
from communication.messageHandling import MessageHandling
from direct.task import Task

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

    def move(self):
        p.resetBaseVelocity(self.boxId, [-self.keys['a']+self.keys['d'], -self.keys['s']+self.keys['w'], self.keys['space']])
        #p.resetBaseVelocity(self.boxId, [-2, 0, 0])

    # def move_foward(self):
    #     p.resetBaseVelocity(self.boxId, [0, 2, 0])

    # def move_left(self):
    #     #(x, y, z)=p.getBaseVelocity(boxId)
    #     p.resetBaseVelocity(self.boxId, [-2, 0, 0])
    #     #p.resetBaseVelocity(boxId, (x, y, z + 4))

    # def move_backward(self):
    #     p.resetBaseVelocity(self.boxId, [0, -2, 0])

    # def move_right(self):
    #     p.resetBaseVelocity(self.boxId, [2, 0, 0])

    # def move_jump(self):
    #     p.resetBaseVelocity(self.boxId, [0, 0, 4])

    def setup(self, renderId):
        self.renderId = renderId
        self.keys = {'a': 0, 'd': 0, 'w': 0, 's': 0, 'space': 0}
        self.physicsClient = p.connect(p.GUI)
        p.setGravity(0, 0, -20)
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
        self.planeId = p.loadURDF("plane.urdf")
        self.startPos = [0, 0, 1]
        self.startOrientation = p.getQuaternionFromEuler([0, 0, 0])
        self.boxId = p.loadURDF("cube.urdf", self.startPos, self.startOrientation)
        #self.start()

    
    def start(self, task):
        #keys = p.getKeyboardEvents()
        self.move()
        pos1, _ = (p.getBasePositionAndOrientation(self.boxId))
        # if ord('w') in keys:
        #     self.move_foward()
        # if ord('a') in keys:
        #     self.move_left()
        # if ord('s') in keys:
        #     self.move_backward()
        # if ord('d') in keys:
        #     self.move_right()
        # if ord(' ') in keys:
        #     if pos[2] < 0.5:
        #         self.move_jump()
        p.stepSimulation()
        #pos2, _ = (p.getBasePositionAndOrientation(self.boxId))
        #MessageHandling().add_message(Message("physics engine", self.renderId, CharacterMove(pos1[0]-pos2[0],pos1[1]-pos2[1],pos1[2]-pos2[2])))
        MessageHandling().add_message(Message("physics engine", self.renderId, CharacterMove(pos1[0],pos1[1],pos1[2])))

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



"""
def recieveMessage()
    if instance of move
        resetBaseVelocity ...
    if instance of remove
    if instance of add

def sendMessage(


"""