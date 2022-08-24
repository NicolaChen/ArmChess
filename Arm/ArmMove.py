import time

from InverseKinematics import IK
from ServoMove import ServoMove


class ArmMove:

    def __init__(self):
        self.servos = ServoMove()
        self.servos.servoMove([[180, 0, 0],
                               [180, 0, 0],
                               [180, 0, 0],
                               [150, 0, 0],
                               [150, 0, 0],
                               [150, 0, 0]])
        self.rot_adjust_2 = 12.5
        self.rot_adjust_3 = -9
        self.rot_adjust_5 = -5
        self.angle_adjust = [185, 90 + self.rot_adjust_2, 90 + self.rot_adjust_3, 420, 150 + self.rot_adjust_2 + self.rot_adjust_3 + self.rot_adjust_5, 0]
        self.ik = IK()
        self.center = [361, 0, 359]
        print("Arm initialize complete.")

    def armCSInit(self):

        print("Begin coordinate system initialization.")
        self.armMove()
        print("Arm has moved to original center point: %s." % self.center)
        while True:
            while True:
                adjust_direction = input("Please input direction you want to adjust to, such as x/y/z.\r\n")
                if adjust_direction in ['x', 'y', 'z']:
                    break
                print("Invalid input! Try again.")
            while True:
                adjust_distance = input("Please input distance you want to adjust with, FLOAT is acceptable.\r\n")
                try:
                    eval(adjust_distance)
                except NameError:
                    print("Invalid input! Not a number.")
                    continue
                if -500 < eval(adjust_distance) < 500:
                    break
                print("Invalid input! Number too big.")
            self.center[['x', 'y', 'z'].index(adjust_direction)] += eval(adjust_distance)
            print("New center: %s" % self.center)
            move_flag = self.armMove()
            if move_flag:
                print("Arm has moved to new center: %s." % self.center)
            else:
                self.center[['x', 'y', 'z'].index(adjust_direction)] -= eval(adjust_distance)
                print("Arm remains previous center: %s." % self.center)
            flag = input("Continue? (y/n)\r\n")
            if flag == 'n':
                break
            else:
                print("Continue arm center adjustment.")
        print("Arm center adjustment complete. Current center point: %s." % self.center)

    def servoMatGen(self, coordinate=None):

        if coordinate == None:
            coordinate = self.center
        res = self.ik.getJointsAngles(coordinate, 270, 180)
        print(res)        # debug
        if res == False:
            return False
        return [[self.angle_adjust[0] + res['rot_j1'], 0, 0],
                [self.angle_adjust[1] + res['rot_j2'], 0, 0],
                [self.angle_adjust[2] + res['rot_j3'], 0, 0],
                [self.angle_adjust[3] - res['rot_j4'], 0, 0],
                [self.angle_adjust[4] - res['rot_j5'], 0, 0],
                [self.angle_adjust[5] + 0, 0, 0]]

    def armMove(self, coordinate=None):

        if coordinate == None:
            coordinate = self.center
        matrix = self.servoMatGen(coordinate)
        if matrix == False:
            print("Can not move to that coordinate.")
            return False
        else:
            self.servos.servoMove(matrix)
            return True

