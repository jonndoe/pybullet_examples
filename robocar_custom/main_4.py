import pybullet as p
from time import sleep

p.connect(p.DIRECT)


car = p.loadURDF('simplecar.urdf')
number_of_joints = p.getNumJoints(car)
for joint_number in range(number_of_joints):
    info = p.getJointInfo(car, joint_number)
    print(info[0], ": ", info[1])


