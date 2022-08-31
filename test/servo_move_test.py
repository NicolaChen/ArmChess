import time
import wiringpi
from wiringpi import GPIO
import sys
sys.path.append('..')

from Servo.ServoMove import ServoMove

s = ServoMove()
wPi = 16
wiringpi.wiringPiSetup()
wiringpi.pinMode(wPi, GPIO.OUTPUT)
i = 0
while True:
    s.servoMove([[150, 0, 0],
                 [120, 0, 0],
                 [220, 0, 0],
                 [40, 0, 0],
                 [70, 0, 0],
                 [100, 0, 0]])
    wiringpi.digitalWrite(wPi, GPIO.HIGH)
    time.sleep(2)

    s.servoMove([[160, 0, 0],
                 [120, 0, 0],
                 [220, 0, 0],
                 [150, 0, 0],
                 [70, 0, 0],
                 [100, 0, 0]])
    wiringpi.digitalWrite(wPi, GPIO.LOW)
    time.sleep(2)
    s.servoMove([[140, 0, 0],
                 [120, 0, 0],
                 [220, 0, 0],
                 [200, 0, 0],
                 [70, 0, 0],
                 [100, 0, 0]])

    time.sleep(2)
    i += 1
    if i > 10:
        break
    

s.closeSerial()
