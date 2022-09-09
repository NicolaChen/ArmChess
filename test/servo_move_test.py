import time
import wiringpi
from wiringpi import GPIO
import sys
sys.path.append('..')

from Servo.ServoMove import ServoMove

s = ServoMove()
#wPi = 16
#wiringpi.wiringPiSetup()
#wiringpi.pinMode(wPi, GPIO.OUTPUT)
i = 0
while True:
    s.servoMove([[180+6, 0, 0],
                 [180-11, 0, 0],
                 [180+3, 0, 0],
                 [150, 0, 0],
                 [30-2, 0, 0],
                 [150, 0, 0]])
#    wiringpi.digitalWrite(wPi, GPIO.HIGH)
    time.sleep(2)

    s.servoMove([[180+6, 0, 0],
                 [180-11, 0, 0],
                 [180+3, 0, 0],
                 [150, 0, 0],
                 [30-2+90, 0, 0],
                 [150, 0, 0]])
#    wiringpi.digitalWrite(wPi, GPIO.LOW)
    time.sleep(2)
    s.servoMove([[180+6, 0, 0],
                 [180-11, 0, 0],
                 [180+3, 0, 0],
                 [150, 0, 0],
                 [30-2+90, 0, 0],
                 [150, 0, 0]])

    time.sleep(2)
    i += 1
    if i > 10:
        break
    

s.closeSerial()
