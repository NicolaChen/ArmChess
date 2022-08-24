import time

from Arm.ArmMove import *

arm = ArmMove()

print("Done")
time.sleep(2)
arm.armCSInit()

while True:
    arm.armMove([300, 50, 127.5])
    time.sleep(2)
    arm.armMove([400, 50, 127.5])
    time.sleep(2)
    arm.armMove([400, -50, 127.5])
    time.sleep(2)
    arm.armMove([300, -50, 127.5])
    time.sleep(2)
