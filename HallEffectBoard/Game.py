import time
from datetime import datetime

import chess

from Arm.ArmMove import ArmMove
from HallEffectBoard.ChessEng import ChessEng
from HallEffectBoard.HallEffectBoard import HallEffectBoard


class Game:

    def __init__(self):
        self.engine_latest_move = None
        self.chess_engine = ChessEng()
        self.is_check = False
        self.winner = ""
        self.over = False
        self.player_move = "Unknown"
        self.player_move_error = False
        self.board_match_error = False
        self.arm = ArmMove()
        self.arm_side = "Unknown"
        self.stop_detect_flag = False
        self.hall_effect_board = HallEffectBoard()

    def setUp(self):
        f = open("ChessRecord.txt", "a+")
        f.write("New chess game at: " + str(datetime.now()) + "\r\n")
        f.close()
        self.arm.armMove()

    def setArmSide(self, side):
        self.arm_side = side

    def isBoardSet(self):
        while True:
            res = self.hall_effect_board.getLine()
            if res[:7] == 'Message' and self.hall_effect_board.board_initialized_flag is True:
                return True
            time.sleep(0.1)

    def engineMove(self):
        """
        Feeds current board to engine; Returns engine's new move
        """
        self.chess_engine.feedToEngine()
        self.is_check = self.chess_engine.engBoard.is_check()
        if self.chess_engine.engBoard.is_checkmate():
            self.winner = "Engine Wins!"
            self.over = True

    def detectPlayerMove(self):
        while True:
            res = self.hall_effect_board.getLine()
            if len(res) == 4 and self.hall_effect_board.move_made_flag is True:
                self.player_move = res
                self.hall_effect_board.resetStatus()
                break
            time.sleep(0.1)

        code = self.chess_engine.updateMove(self.player_move)
        if code == 1:
            # illegal move prompt GUI to open Player Move Error Page
            self.player_move_error = True
        else:
            self.player_move_error = False
            # write to Game.txt file
            f = open("ChessRecord.txt", "a+")
            f.write(chess.Move.from_uci(self.player_move).uci() + "\r\n")
            f.close()
        # check for Game Over
        if self.chess_engine.engBoard.is_checkmate():
            self.winner = "You win!"
            self.over = True

    def checkEngineMove(self):
        while True:
            res = self.hall_effect_board.getLine()
            if len(res) == 4 and self.hall_effect_board.move_made_flag is True:
                detect_move = res
                self.hall_effect_board.resetStatus()
                break
            time.sleep(0.1)
        if detect_move != self.engine_latest_move.uci():
            print("D: " + detect_move + "\nE: " + self.engine_latest_move.uci())
            self.board_match_error = True
        else:
            self.board_match_error = False

    def playerPromotion(self, move):
        print(move)
        code = self.chess_engine.updateMove(move)
        if code == 1:
            # illegal move prompt GUI to open PlayerMoveError Page
            print("Error")
            self.player_move_error = True
        else:
            self.player_move_error = False

            # write to Game.txt file
            f = open("ChessRecord.txt", "a+")
            f.write(chess.Move.from_uci(move).uci() + "\r\n")
            f.close()

        # check Game Over
        if self.chess_engine.engBoard.is_checkmate():
            self.winner = "You win!"
            self.over = True

    def moveChess(self):

        medium = 15
        high = 30
        h0 = h1 = 5
        self.engine_latest_move = self.chess_engine.engine_move
        piece_0 = str(self.chess_engine.engBoard.piece_at(chess.parse_square(self.engine_latest_move.uci()[:2])))
        piece_1 = str(self.chess_engine.engBoard.piece_at(chess.parse_square(self.engine_latest_move.uci()[2:4])))
        if piece_0.upper() in ["K", "Q"]:
            h0 = high
        elif piece_0.upper() in ["B", "N", "R"]:
            h0 = medium
        if piece_1.upper() in ["K", "Q"]:
            h1 = high
        elif piece_1.upper() in ["B", "N", "R"]:
            h1 = medium
        if self.chess_engine.engBoard.is_en_passant(chess.Move.from_uci(self.engine_latest_move.uci())):
            self.arm.armMoveChess(self.arm_side, self.engine_latest_move.uci(),
                                  piece_0, piece_1, 1)
        elif len(self.engine_latest_move.uci()) == 5:
            piece_promo = self.engine_latest_move.uci()[-1]
            if piece_promo == "q":
                h2 = high
                promo_code = 1
            else:
                h2 = medium
                if piece_promo == "r":
                    promo_code = 2
                elif piece_promo == "b":
                    promo_code = 3
                else:
                    promo_code = 4
            if self.chess_engine.engBoard.is_capture(chess.Move.from_uci(self.engine_latest_move.uci())):
                self.arm.armMoveChess(self.arm_side, self.engine_latest_move.uci(),
                                      piece_0, piece_1, 0, 1, promo_code, h0, h1, h2)
            else:
                self.arm.armMoveChess(self.arm_side, self.engine_latest_move.uci(), 0, 0, promo_code, h0, h1, h2)
        elif self.chess_engine.engBoard.is_capture(chess.Move.from_uci(self.engine_latest_move.uci())):
            self.arm.armMoveChess(self.arm_side, self.engine_latest_move.uci(),
                                  piece_0, piece_1, 0, 1, 0, h0, h1)
        else:
            self.arm.armMoveChess(self.arm_side, self.engine_latest_move.uci(),
                                  piece_0, piece_1, 0, 0, 0, h0)
