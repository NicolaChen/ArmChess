import wiringpi
from wiringpi import GPIO
wPi = 13


class Pump:

    def __init__(self):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(wPi, GPIO.OUTPUT)
        self.release()

    @staticmethod
    def capture():
        wiringpi.digitalWrite(wPi, GPIO.HIGH)

    @staticmethod
    def release():
        wiringpi.digitalWrite(wPi, GPIO.LOW)
