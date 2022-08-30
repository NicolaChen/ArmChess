import time

import numpy as np

from Arm.InverseKinematics import IK
from Arm.Pump import Pump
from Servo.ServoMove import ServoMove


class ArmMove:

    def __init__(self):
        self.servos = ServoMove()
        self.servos.servoMove([[180 + 4.1 + 0.9, 0, 0],
                               [180 + 12.7, 0, 0],
                               [180 - 10, 0, 0],
                               [150, 0, 0],
                               [150 - 1.5, 0, 0],
                               [150, 0, 0]])
        self.rot_adjust_2 = 12.7
        self.rot_adjust_3 = -10
        self.rot_adjust_5 = -1.5
        self.angle_adjust = [180 + 4.1 + 0.9, 90 + self.rot_adjust_2, 90 + self.rot_adjust_3, 420,
                             150 + self.rot_adjust_5, 0]
        self.ik = IK()
        self.center = [170, 0, 140]
        self.board_matrix = np.load("./test/chess_board_matrix.npy")
        self.outSpaceCnt = 0
        self.pump = Pump()
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

        if coordinate is None:
            coordinate = self.center
        res = self.ik.getJointsAngles(coordinate, 270, 180)
        print(res)  # debug
        if not res:
            return False
        return [[self.angle_adjust[0] - res['rot_j1'], 0, 0],
                [self.angle_adjust[1] + res['rot_j2'], 0, 0],
                [self.angle_adjust[2] + res['rot_j3'], 0, 0],
                [self.angle_adjust[3] - res['rot_j4'], 0, 0],
                [self.angle_adjust[4] - res['rot_j5'], 0, 0],
                [self.angle_adjust[5] + 0, 0, 0]]

    def armMove(self, coordinate=None):

        if coordinate is None:
            coordinate = self.center
        matrix = self.servoMatGen(coordinate)
        if not matrix:
            print("Can not move to that coordinate.")
            return False
        else:
            self.servos.servoMove(matrix)
            return True

    def armMoveChess(self, arm_side, uci_move, en_passant_flag=0, capture_flag=0):

        if capture_flag:
            self.moveChess_out(arm_side, uci_move[2:], self.outSpaceManagement())
        # in-board move
        self.moveChess_in(arm_side, uci_move)

        # special condition
        if en_passant_flag:
            self.moveChess_out(arm_side, uci_move[0] + uci_move[3], self.outSpaceManagement())
        elif uci_move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']:
            if uci_move == 'e1g1':
                self.moveChess_in(arm_side, 'h1f1')
            elif uci_move == 'e1c1':
                self.moveChess_in(arm_side, 'a1d1')
            elif uci_move == 'e8g8':
                self.moveChess_in(arm_side, 'h8f8')
            else:
                self.moveChess_in(arm_side, 'a8d8')
        # arm return to center
        self.armMove(self.center)

    def moveChess_in(self, arm_side, uci_move):

        col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if arm_side == 'Black':
            i0 = 7 - col.index(uci_move[0])
            j0 = 8 - eval(uci_move[1])
            i1 = 7 - col.index(uci_move[2])
            j1 = 8 - eval(uci_move[3])
        else:
            i0 = col.index(uci_move[0])
            j0 = eval(uci_move[1]) - 1
            i1 = col.index(uci_move[2])
            j1 = eval(uci_move[3]) - 1
        self.armMove([self.board_matrix[i0][j0][0], self.board_matrix[i0][j0][1], 100])
        self.armMove([self.board_matrix[i0][j0][0], self.board_matrix[i0][j0][1], 15])
        self.pump.capture()
        time.sleep(0.5)
        self.armMove([self.board_matrix[i0][j0][0], self.board_matrix[i0][j0][1], 100])
        self.armMove([self.board_matrix[i1][j1][0], self.board_matrix[i1][j1][1], 100])
        self.armMove([self.board_matrix[i1][j1][0], self.board_matrix[i1][j1][1], 15])
        self.pump.release()
        time.sleep(1.5)
        self.armMove([self.board_matrix[i1][j1][0], self.board_matrix[i1][j1][1], 100])

    def moveChess_out(self, arm_side, ori_pos, des_pos):

        col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if type(ori_pos) == str:
            if arm_side == 'Black':
                i0 = 7 - col.index(ori_pos[0])
                j0 = 8 - eval(ori_pos[1])
            else:
                i0 = col.index(ori_pos[0])
                j0 = eval(ori_pos[1]) - 1
            i1, j1 = des_pos
            self.armMove([self.board_matrix[i0][j0][0], self.board_matrix[i0][j0][1], 100])
            self.armMove([self.board_matrix[i0][j0][0], self.board_matrix[i0][j0][1], 15])
            self.pump.capture()
            self.armMove([self.board_matrix[i0][j0][0], self.board_matrix[i0][j0][1], 100])
            time.sleep(1)
            self.armMove([i1, j1, 100])
            self.armMove([i1, j1, 15])
            self.pump.release()
            self.armMove([i1, j1, 100])
        else:
            i0, j0 = ori_pos
            if arm_side == 'Black':
                i1 = 7 - col.index(des_pos[0])
                j1 = 8 - eval(des_pos[1])
            else:
                i1 = col.index(des_pos[0])
                j1 = eval(des_pos[1]) - 1
            self.armMove([i0, j0, 100])
            self.armMove([i0, j0, 15])
            self.pump.capture()
            self.armMove([i0, j0, 100])
            time.sleep(1)
            self.armMove([self.board_matrix[i1][j1][0], self.board_matrix[i1][j1][1], 100])
            self.armMove([self.board_matrix[i1][j1][0], self.board_matrix[i1][j1][1], 15])
            self.pump.release()
            self.armMove([self.board_matrix[i1][j1][0], self.board_matrix[i1][j1][1], 100])

    def outSpaceManagement(self):

        x = 200
        y = -200  # temporary set fixed
        self.outSpaceCnt += 1
        return x, y
