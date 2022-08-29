import wiringpi
from wiringpi import GPIO


class Pump:

    def __init__(self):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(5, GPIO.OUTPUT)
        self.release()

    @staticmethod
    def capture():
        wiringpi.digitalWrite(5, GPIO.HIGH)

    @staticmethod
    def release():
        wiringpi.digitalWrite(5, GPIO.LOW)
