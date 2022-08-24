import time

from ServoMove import ServoMove

s = ServoMove()
i = 0
while True:
    s.servoMove([[180, 0, 0],
                 [180, 0, 0],
                 [180, 0, 0],
                 [150, 0, 0],
                 [150, 0, 0],
                 [150, 0, 0]])

    time.sleep(2)

    s.servoMove([[180, 0, 0],
                 [220, 0, 0],
                 [140, 0, 0],
                 [150, 0, 0],
                 [150, 0, 0],
                 [150, 0, 0]])
    time.sleep(2)
    i += 1
    if i > 5:
        break

s.closeSerial()
