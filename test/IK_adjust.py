import time
import sys
import numpy as np
sys.path.append('..')

from Arm.ArmMove import *

arm = ArmMove()

print("Initialization Done")

while True:
    cord = [200, 0, 200]    
    arm.armMove(cord)
    test_cord_1 = input("Coordinate 1: ")
    test_cord_2 = input("Coordinate 2: ")
    cnt = 0
    while True:
        if test_cord_1 == '' or test_cord_2 == '':
            break
        cord_1 = eval(test_cord_1)
        cord_2 = eval(test_cord_2)
        arm.armMove(cord_1)
        time.sleep(0.5)
        arm.armMove(cord_2)
        time.sleep(0.5)
        cnt += 1
        if cnt > 20:
            break
