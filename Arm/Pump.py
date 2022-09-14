import time
import wiringpi
from wiringpi import GPIO
pump = 16
valve = 15


class Pump:

    def __init__(self):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(pump, GPIO.OUTPUT)
        wiringpi.digitalWrite(pump, GPIO.LOW)
        wiringpi.pinMode(valve, GPIO.OUTPUT)
        wiringpi.digitalWrite(valve, GPIO.LOW)

    @staticmethod
    def capture():
        wiringpi.digitalWrite(pump, GPIO.HIGH)
        time.sleep(0.5)
        wiringpi.digitalWrite(valve, GPIO.HIGH)
        wiringpi.digitalWrite(pump, GPIO.LOW)
    @staticmethod
    def release():
        wiringpi.digitalWrite(valve, GPIO.LOW)
