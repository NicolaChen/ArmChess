import time

import numpy as np
import serial

from Servo.pwm_servo.PCA9685 import PCA9685
from Servo.uart_servo.MyCheckSum import MyCheckSum as CheckSum


class ServoMove:

    def __init__(self):
        self.step_range = [4096, 0, 0, 1024, 1000, 1024]
        self.angle_range = [360, 360, 360, 300, 240, 300]
        self.servo_type = ["FTT", "PWM", "PWM", "FTC", "HW", "FTC"]
        self.servo_angle = [185, 128.96505375285784, 240.23068603953044, 150, 64.99573979238826, 0]

        self.serial = serial.Serial('/dev/ttyS4', 115200)
        self.pwm = PCA9685(0x40)
        self.pwm.setPWMFreq(50)

    def servoMove(self, angle_matrix):  # TODO: Figure out how duration and speed affect FTT/FTC

        old_angle_2 = self.servo_angle[1]
        old_angle_3 = self.servo_angle[2]
        angle_2 = angle_matrix[1][0]
        angle_3 = angle_matrix[2][0]
        time_gap = 0.025
        delta_x = 0.1

        for p in np.arange(np.pi / -2, np.pi / 2, delta_x):
            serial_write_buf = []

            for i in [0, 3, 4, 5]:
                ori_angle = self.servo_angle[i]
                aim_angle = angle_matrix[i][0]
                if aim_angle > self.angle_range[i]:
                    aim_angle = self.angle_range[i]
                elif aim_angle < 0:
                    aim_angle = 0

                step = round(self.step_range[i] * (ori_angle + (aim_angle - ori_angle) * (np.sin(p) + 1) / 2) /
                             self.angle_range[i])
                if self.servo_type[i] == "FTT":
                    buf_t = bytes(self.ftMoveT(i + 1, step, angle_matrix[i][1], angle_matrix[i][2]))
                    for j in buf_t:
                        serial_write_buf.append(j)
                elif self.servo_type[i] == "FTC":
                    buf_c = bytes(self.ftMoveC(i + 1, step, angle_matrix[i][1], angle_matrix[i][2]))
                    for k in buf_c:
                        serial_write_buf.append(k)
                elif self.servo_type[i] == "HW":
                    buf_h = bytes(self.hwMove(i + 1, step, angle_matrix[i][1]))
                    for h in buf_h:
                        serial_write_buf.append(h)
                else:
                    print("Servo%2d move fail!" % (i + 1))
            pulse_2 = 2000 * (old_angle_2 + (angle_2 - old_angle_2) * (np.sin(p) + 1) / 2) / self.angle_range[1] + 500
            pulse_3 = 2000 * (old_angle_3 + (angle_3 - old_angle_3) * (np.sin(p) + 1) / 2) / self.angle_range[2] + 500
            self.pwm.setServoPulse(0, pulse_2)
            self.pwm.setServoPulse(1, pulse_3)
            self.serial.write(serial_write_buf)

            time.sleep(time_gap)

        for i in range(6):
            self.servo_angle[i] = angle_matrix[i][0]
        # print(self.servo_angle)

    def getTherm(self):
        buf_1 = bytes(self.ftRead(1, 0x3F, 0x01))
        self.serial.write(buf_1)
        print("Now reading servo1 temperature.")
        while True:
            if self.serial.in_waiting:
                res = self.serial.read(size=7)
                break
        print(res)

    @staticmethod
    def getLowByte(val):
        return int(bin(val & 0xFF)[2:], 2)

    @staticmethod
    def getHighByte(val):
        return int(bin(val >> 8)[2:], 2)

    def ftMoveT(self, n, p, t, v):
        buf = [0 for _ in range(13)]
        buf[0] = buf[1] = 0xFF
        buf[2] = n
        buf[3] = 0x09
        buf[4] = 0x03
        buf[5] = 0x2A
        buf[6] = self.getLowByte(p)
        buf[7] = self.getHighByte(p)
        buf[8] = self.getLowByte(t)
        buf[9] = self.getHighByte(t)
        buf[10] = self.getLowByte(v)
        buf[11] = self.getHighByte(v)
        buf[12] = int(CheckSum(buf[2:-1]).get()[2:], 16)
        return buf

    def ftMoveC(self, n, p, t, v):
        buf = [0 for _ in range(13)]
        buf[0] = buf[1] = 0xFF
        buf[2] = n
        buf[3] = 0x09
        buf[4] = 0x03
        buf[5] = 0x2A
        buf[6] = self.getHighByte(p)
        buf[7] = self.getLowByte(p)
        buf[8] = self.getHighByte(t)
        buf[9] = self.getLowByte(t)
        buf[10] = self.getHighByte(v)
        buf[11] = self.getLowByte(v)
        buf[12] = int(CheckSum(buf[2:-1]).get()[2:], 16)
        return buf

    @staticmethod
    def ftRead(n, address, val_len):
        buf = [0 for _ in range(8)]
        buf[0] = buf[1] = 0xFF
        buf[2] = n
        buf[3] = 0x04
        buf[4] = 0x02
        buf[5] = address
        buf[6] = val_len
        buf[7] = int(CheckSum(buf[2:-1]).get()[2:], 16)
        return buf

    def hwMove(self, n, p, t):
        buf = [0 for _ in range(10)]
        buf[0] = buf[1] = 0x55
        buf[2] = n
        buf[3] = 7
        buf[4] = 1
        buf[5] = self.getLowByte(p)
        buf[6] = self.getHighByte(p)
        buf[7] = self.getLowByte(t)
        buf[8] = self.getHighByte(t)
        buf[9] = int(CheckSum(buf[2:-1]).get()[2:], 16)
        return buf

    def closeSerial(self):
        self.serial.close()
        print("Serial has been closed!")
