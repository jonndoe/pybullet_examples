import pybullet as p
import pybullet_data


client = p.connect(p.GUI)
p.setGravity(0,0, -10, physicsClientId=client)

p.setAdditionalSearchPath(pybullet_data.getDataPath())
planedId = p.loadURDF("plane.urdf")

carId = p.loadURDF('racecar/racecar.urdf', basePosition=[0,0,0.2])

position, orientation = p.getBasePositionAndOrientation(carId)





for _ in range(300): 
    pos, ori = p.getBasePositionAndOrientation(carId)
    p.applyExternalForce(carId, 0, [50, 0, 0], position, p.WORLD_FRAME)
    p.stepSimulation()


while True:
    pass
