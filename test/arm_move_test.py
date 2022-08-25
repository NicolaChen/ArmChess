import time
import sys
sys.path.append('..')

from Arm.ArmMove import *

arm = ArmMove()

print("Done")
time.sleep(5)
# arm.armCSInit()

while True:
    arm.armMove([200, 0, 40])
    time.sleep(2)
    arm.armMove([200, -130, 40])
    time.sleep(2)
    arm.armMove([200, 130, 40])
    time.sleep(2)
    arm.armMove([200, 0, 40])
    time.sleep(2)
    arm.armMove([300, 0, 40])
    time.sleep(2)
    arm.armMove([300, -130, 40])
    time.sleep(2)
    arm.armMove([300, 130, 40])
    time.sleep(2)
    arm.armMove([300, 0, 40])
    time.sleep(2)
    arm.armMove([450, 0, 40])
    time.sleep(2)
    arm.armMove([450, -130, 40])
    time.sleep(2)
    arm.armMove([450, 130, 40])
    time.sleep(2)
    arm.armMove([450, 0, 40])
    time.sleep(2)
