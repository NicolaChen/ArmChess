import time

from Servo.ServoMove import ServoMove

s = ServoMove()
i = 0
s.servoMove([[180, 0, 0],
             [180, 0, 0],
             [0, 0, 0],
             [150, 0, 0],
             [150, 0, 0],
             [150, 0, 0]])
time.sleep(2)
s.servoMove([[180, 0, 0],
             [180, 0, 0],
             [90, 0, 0],
             [150, 0, 0],
             [150, 0, 0],
             [150, 0, 0]])
time.sleep(2)
s.servoMove([[180, 0, 0],
             [180, 0, 0],
             [180, 0, 0],
             [150, 0, 0],
             [150, 0, 0],
             [150, 0, 0]])
time.sleep(2)
s.servoMove([[180, 0, 0],
             [180, 0, 0],
             [270, 0, 0],
             [150, 0, 0],
             [150, 0, 0],
             [150, 0, 0]])
time.sleep(2)
s.servoMove([[180, 0, 0],
             [180, 0, 0],
             [180, 0, 0],
             [150, 0, 0],
             [150, 0, 0],
             [150, 0, 0]])

s.closeSerial()
