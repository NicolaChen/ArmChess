import time
import sys
sys.path.append('..')

from Arm.ArmMove import *

arm = ArmMove()

print("Done")
time.sleep(2)
# arm.armCSInit()

while True:
    arm.armMove([200, 0, 107.5])
    time.sleep(2)
    arm.armMove([200, -130, 107.5])
    time.sleep(2)
    arm.armMove([200, 130, 107.5])
    time.sleep(2)
    arm.armMove([200, 0, 107.5])
    time.sleep(2)
    arm.armMove([300, 0, 107.5])
    time.sleep(2)
    arm.armMove([300, -130, 107.5])
    time.sleep(2)
    arm.armMove([300, 130, 107.5])
    time.sleep(2)
    arm.armMove([300, 0, 107.5])
    time.sleep(2)
    arm.armMove([450, 0, 107.5])
    time.sleep(2)
    arm.armMove([450, -130, 107.5])
    time.sleep(2)
    arm.armMove([450, 130, 107.5])
    time.sleep(2)
    arm.armMove([450, 0, 107.5])
    time.sleep(2)
