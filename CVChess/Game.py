import threading
import time
from datetime import datetime

import chess
import cv2

from Arm.ArmMove import ArmMove
from CVChess.BoardRecognition import BoardRecognition
from CVChess.Camera import Camera
from CVChess.ChessEng import ChessEng


class Game:

    def __init__(self):
        self.camera = Camera()
        self.board = None
        self.board_perimeter = 0
        self.contour_threshold = 200
        self.current = None
        self.previous = None
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
        self.threshold_adjust = 10

    def setUp(self):
        """
        Prepares camera thread and start it; Writes new beginning to txt file
        """
        cam_thread = threading.Thread(target=self.camera.run)
        cam_thread.setDaemon(True)
        cam_thread.start()

        f = open("ChessRecord.txt", "a+")
        f.write("New chess game at: " + str(datetime.now()) + "\r\n")
        f.close()
        self.arm.armMove()

    def caliCam(self):
        """
        Simply shows camera images
        """
        self.camera.cali()

    def analyzeBoard(self):
        """
        Finds chessboard squares and assigns their states
        """
        board_recognize = BoardRecognition(self.camera)
        while True:
            self.board = board_recognize.initializeBoard(self.threshold_adjust)
            if not board_recognize.recog_fail_flag and self.board:
                break
            else:
                print("Board recognize fail,try again...")
        self.board.assignState()
        self.board_perimeter = board_recognize.contour_perimeter

    def isBoardSet(self):
        """
        Gets one clear image of board from camera
        """
        time.sleep(2)  # Give camera some time to focus, can be dismissed
        while True:
            self.current = self.camera.getFrame()
            if abs(cv2.Laplacian(self.current, cv2.CV_64F).var() - self.camera.laplacian_threshold) < 80:
                break

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
        """
        Detects player moves from images, get previous image and current image
        """
        self.previous = self.current
        begin_cnt = 0
        while True:
            # detects player's hand/tool invasion into board border
            image = self.camera.getFrame()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (11, 11), 0)
            ret1, th1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            ret2, th2 = cv2.threshold(blur, ret1+self.threshold_adjust, 255, cv2.THRESH_BINARY)
            max_contour, square_scale, contour_perimeter = BoardRecognition.getContour(image, th2)
            if self.stop_detect_flag:
                print("STOP DETECT")
                self.stop_detect_flag = True
                return 0
            if abs(self.board_perimeter - contour_perimeter) > self.contour_threshold:
                print("Detect object invasion")
                begin_cnt += 1
                if begin_cnt >= 2:
                    break
        end_cnt = 0
        while True:
            # detects end of invasion， 10 times make sure
            self.current = self.camera.getFrame()
            gray = cv2.cvtColor(self.current, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (11, 11), 0)
            ret1, th1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            ret2, th2 = cv2.threshold(blur, ret1+self.threshold_adjust, 255, cv2.THRESH_BINARY)
            max_contour, square_scale, contour_perimeter = BoardRecognition.getContour(self.current, th2)
            if self.stop_detect_flag:
                print("STOP DETECT")
                self.stop_detect_flag = True
                return 0
            if abs(self.board_perimeter - contour_perimeter) < self.contour_threshold:
                print("Detect invasion finish")
                end_cnt += 1
                if end_cnt >= 10:
                    break
            else:
                print("Invasion exist")
        self.playerMove()

    def playerMove(self, insert_move=None):
        """
        Finds difference between previous and current, deduces player's move and updates move to engine
        """
        if insert_move is None:
            self.player_move = self.board.determineChanges(self.previous, self.current)
        else:
            self.player_move = insert_move
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

    def updateCurrent(self):
        self.previous = self.current
        for i in range(10):
            self.current = self.camera.getFrame()
            if abs(cv2.Laplacian(self.current, cv2.CV_64F).var() - self.camera.laplacian_threshold) < 80:
                break

    def checkEngineMove(self):
        detect_move = self.board.determineChanges(self.previous, self.current)
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

    def setArmSide(self, side):
        self.arm_side = side

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

    def updatePrevious(self):
        """
        Update previous frame in case identify errors caused by unexpected moves
        """
        time.sleep(2)
        frame = None
        for _ in range(20):
            frame = self.camera.getFrame()
            if abs(cv2.Laplacian(frame, cv2.CV_64F).var() - self.camera.laplacian_threshold) < 50:
                break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11, 11), 0)
        ret1, th1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        ret2, th2 = cv2.threshold(blur, ret1+self.threshold_adjust, 255, cv2.THRESH_BINARY)
        _, _, self.board_perimeter = BoardRecognition.getContour(frame, th2)
        print("Update previous frame success.")
        self.current = frame
