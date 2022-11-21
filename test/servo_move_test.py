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
    #s.servoMove([[180+6, 0, 0],
    #             [180-11-10, 0, 0],
    #             [180+3, 0, 0],
    #             [150, 0, 0],
    #             [30-2, 0, 0],
    #             [150, 0, 0]])
#    wiringpi.digitalWrite(wPi, GPIO.HIGH)
    #time.sleep(2)

    #s.servoMove([[180+6, 0, 0],
    #             [180-11-30, 0, 0],
    #             [180+3-30, 0, 0],
    #             [150, 0, 0],
    #             [30-2+90, 0, 0],
    #             [150, 0, 0]])
#    wiringpi.digitalWrite(wPi, GPIO.LOW)
    #time.sleep(2)
    #s.servoMove([[180+6, 0, 0],
    #             [180-11-50, 0, 0],
    #             [180+3+30, 0, 0],
    #             [150, 0, 0],
    #             [30-2+90, 0, 0],
    #             [150, 0, 0]])
    k_in = input("input angle matrix\r\n")
    if k_in == '' or k_in == 'n':
        break
    t_in = eval(k_in)
    s.servoMove([[180+6, 0, 0],
                 [t_in[0], 0, 0],
                 [t_in[1], 0, 0],
                 [150, 0, 0],
                 [30-2, 0, 0],
                 [150, 0, 0]])
    time.sleep(2)
    i += 1
    if i > 10:
        break
    

s.closeSerial()
