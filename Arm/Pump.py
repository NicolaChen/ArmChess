import wiringpi
from wiringpi import GPIO
wPi = 16


class Pump:

    def __init__(self):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(wPi, GPIO.OUTPUT)
        wiringpi.digitalWrite(wPi, GPIO.LOW)

    @staticmethod
    def capture():
        wiringpi.digitalWrite(wPi, GPIO.HIGH)

    @staticmethod
    def release():
        wiringpi.digitalWrite(wPi, GPIO.LOW)
