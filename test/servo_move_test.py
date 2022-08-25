import time
import sys
sys.path.append('..')

from Servo.ServoMove import ServoMove

s = ServoMove()
# i = 0
while True:
    s.servoMove([[200, 0, 0],
                 [110, 0, 0],
                 [260, 0, 0],
                 [150, 0, 0],
                 [70, 0, 0],
                 [100, 0, 0]])

    time.sleep(2)

    s.servoMove([[180 + 4.1, 0, 0],
                 [180 + 12.7, 0, 0],
                 [180 - 10, 0, 0],
                 [150, 0, 0],
                 [150 -1.5, 0, 0],
                 [150, 0, 0]])
    time.sleep(3)
    s.servoMove([[180 + 4.1, 0, 0],
                 [180 + 12.7, 0, 0],
                 [180 - 10, 0, 0],
                 [150, 0, 0],
                 [150 -1.5, 0, 0],
                 [150, 0, 0]])
    # time.sleep(5)
    # i += 1
    # if i > 5:
        # break
    a = input("Continue?")
    if a == 'y':
        continue
    elif a == 'n':
        break
    else:
        pass

s.closeSerial()
