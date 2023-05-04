import pybullet as p
import pybullet_data
import time

physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -10)
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
planeId = p.loadURDF("plane.urdf")
startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])
boxId = p.loadURDF("r2d2.urdf", startPos, startOrientation)

def move_right():
    p.resetBaseVelocity(boxId, [-1, 0, 0])

def move_left():
    #(x, y, z)=p.getBaseVelocity(boxId)
    p.resetBaseVelocity(boxId, [1, 1, 4])
    #p.resetBaseVelocity(boxId, (x, y, z + 4))

    
for i in range(10000000000000):
    keys = p.getKeyboardEvents()
    if ord('d') in keys:
        move_right()
    if ord('a') in keys:
        move_left()
    p.stepSimulation()
    object_pos, object_ori = p.getBasePositionAndOrientation(boxId)
    plane_pos, plane_ori = p.getBasePositionAndOrientation(planeId)
    print("Object Position: ", object_pos)
    print("Object Orientation: ", object_ori)
    print("Plane Position: ", plane_pos)
    print("Plane Orientation: ", plane_ori)
    if (i % 240 == 0):
        # boxId = p.loadURDF("r2d2.urdf", startPos, startOrientation)
        pass
    time.sleep(1./120)
p.disconnect()



"""
def recieveMessage()
    if instance of move
        resetBaseVelocity ...
    if instance of remove
    if instance of add

def sendMessage(


"""