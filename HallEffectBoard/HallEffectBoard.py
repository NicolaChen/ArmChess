import serial


class HallEffectBoard:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS4', 115200)
        self.previous_move = None
        self.latest_move = None
        self.board_initialized_flag = False
        self.move_made_flag = False
        self.error_move_flag = False

    def getLine(self):
        """
        无限循环读取串口，直到获得信息，返回信息（将去除末尾换行符）
        """
        while True:
            message = self.ser.readline().decode()
            message_length = len(message)
            if message_length == 20:
                self.board_initialized_flag = True
                return message[:-2]
            elif message_length == 4:
                self.move_made_flag = False
                return message[:-2]
            elif message_length == 6:
                self.move_made_flag = True
                self.previous_move = self.latest_move
                self.latest_move = message[:-2]
                return message[:-2]
            elif message_length != 0:
                self.error_move_flag = True
                return message[:-2]
            else:
                continue

    def checkBoardSet(self):
        """
        检查棋盘初始化摆放情况，串口发送"check"，等待示意完成的字符串
        """
        self.ser.write("check")
        res = self.getLine()
        return res

    def startGame(self):
        """
        开始棋盘检测
        """
        self.ser.write("start")
        print("hall effect board start detect...\n")

    def resetStatus(self):
        self.move_made_flag = False
        self.error_move_flag = False
