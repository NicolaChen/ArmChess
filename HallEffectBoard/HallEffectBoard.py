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
        while 1:
            message = self.ser.readline().decode()
            message_length = len(message)
            if message_length == 21:
                self.board_initialized_flag = False
                return message[:-2]
            elif message_length == 20:
                self.board_initialized_flag = True
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

    def resetStatus(self):
        self.move_made_flag = False
        self.error_move_flag = False
