import threading
import time
import tkinter as tk
from tkinter import *

from CVChess.Game import Game

LARGE_FONT = ("system", 50)
MED_FONT = ("system", 30)
SMALL_FONT = ("system", 20)


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        gui = tk.Frame(self)
        gui.pack(side='top', fill="both", expand=True)
        gui.grid_rowconfigure(0, weight=1)
        gui.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.game = Game()
        self.move = StringVar()
        self.move.set("e2e4")
        self.winner = StringVar()
        self.winner.set("Engine Wins!")
        self.error_cnt = 0

        for F in (StartGamePage, InitializePage, SetBoardPage, ChooseDifficultyPage, ChooseColorPage, PlayerMovePage,
                  EngineMovePage, ConfirmPage, GameOverPage, ChoosePromotionPage, PlayerMoveErrorPage, InCheckPage,
                  BoardMatchErrorPage, UpdatePreviousPage):
            frame = F(gui, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartGamePage)

    def showFrame(self, f):
        frame = self.frames[f]
        frame.tkraise()
        if hasattr(frame, 'run'):
            frame.run()

    def destroyFrame(self):
        pass  # TODO: Figure out how to kill the program


# TODO: Adjust every label and button pack
class StartGamePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title_label = tk.Label(self, text="ArmChess with Computer Vision", fg="blue", font=LARGE_FONT)
        title_label.pack(anchor='center', pady=120)

        start_button = tk.Button(self, text="Start Chess Game", fg="green", font=MED_FONT,
                                 command=lambda: [controller.showFrame(ChooseColorPage), controller.game.setUp()])
        start_button.pack(anchor='center', pady=100)


class ChooseColorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        color_label = tk.Label(self, text="Please choose your color", font=LARGE_FONT)
        color_label.pack(pady=80)

        white_button = tk.Button(self, text="White(Blue)", font=MED_FONT, fg="white",
                                 command=lambda: [controller.showFrame(InitializePage),
                                                  controller.game.setArmSide('Black')])
        white_button.pack(pady=80)
        black_button = tk.Button(self, text="Black(Red)", font=MED_FONT,
                                 command=lambda: [controller.showFrame(InitializePage),
                                                  controller.game.setArmSide('White'),
                                                  controller.game.camera.flip()])
        black_button.pack(pady=50)


class InitializePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        cali_label = tk.Label(self, text="Please set a clear board\nwith correct direction", font=LARGE_FONT)
        cali_label.pack(pady=50)
        cali_cam_button = tk.Button(self, text="View camera images to adjust board", font=MED_FONT,
                                    command=lambda: [controller.game.caliCam()])
        cali_cam_button.pack(pady=80)

        init_board_button = tk.Button(self, text="Done", font=MED_FONT,
                                      command=lambda: [controller.showFrame(SetBoardPage),
                                                       controller.game.analyzeBoard()])
        init_board_button.pack(pady=50)


class SetBoardPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        set_board_label = tk.Label(self, text="Please set the BOARD", font=LARGE_FONT)
        set_board_label.pack(pady=50)

        difficulty_button = tk.Button(self, text="Done", font=MED_FONT,
                                      command=lambda: [controller.showFrame(ChooseDifficultyPage),
                                                       controller.game.isBoardSet()])
        difficulty_button.pack(pady=150)


class ChooseDifficultyPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        choose_difficulty_label = tk.Label(self, text="Please choose difficulty", font=LARGE_FONT)
        choose_difficulty_label.pack(pady=50)

        tk.Button(self, text="Easy", font=MED_FONT,
                  command=lambda: [self.setEasy(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=10)
        tk.Button(self, text="Intermediate", font=MED_FONT,
                  command=lambda: [self.setEasy(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=10)
        tk.Button(self, text="Hard", font=MED_FONT,
                  command=lambda: [self.setEasy(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=10)
        tk.Button(self, text="Extreme", font=MED_FONT,
                  command=lambda: [self.setEasy(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=10)
        tk.Button(self, text="Master", font=MED_FONT,
                  command=lambda: [self.setEasy(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=10)

    @staticmethod
    def setEasy(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 0})
        controller.game.chess_engine.time = 0.01

    @staticmethod
    def setIntermediate(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 5})
        controller.game.chess_engine.time = 0.1

    @staticmethod
    def setHard(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 10})
        controller.game.chess_engine.time = 1

    @staticmethod
    def setExtreme(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 15})
        controller.game.chess_engine.time = 3

    @staticmethod
    def setMaster(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 20})
        controller.game.chess_engine.time = 5


class PlayerMovePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        start_label = tk.Label(self, text="Please make your MOVE", fg="green", font=LARGE_FONT)
        start_label.pack(pady=50)

        resign_button = tk.Button(self, text="Resign", font=MED_FONT,
                                  command=lambda: [controller.showFrame(ConfirmPage)])
        resign_button.pack(pady=50)

        show_move_label = tk.Label(self, text="Detect your move is:", font=MED_FONT)
        show_move_label.pack(pady=20)

        self.text = StringVar()
        player_move_label = tk.Label(self, textvariable=self.text, font=LARGE_FONT)
        player_move_label.pack(pady=20)

        move_input_label = tk.Label(self, text="Or you can manually input your move in UCI: ", font=LARGE_FONT)
        move_input_label.pack(pady=40)

        self.input_text = tk.Text(self, height=2)
        self.input_text.pack(pady=20)

        get_input_button = tk.Button(self, text="Insert", font=MED_FONT, command=lambda: [controller.insertText()])
        get_input_button.pack(pady=20)

        self.ctr = controller

    def insertText(self):
        insert_text = self.input_text.get("1.0", "end-1c")
        self.ctr.game.playerMove(insert_text)
        self.text.set(self.ctr.game.player_move)
        self.after(2000, self.checkValid_P)

    def run(self):
        self.text.set("Waiting for your move ...")
        # self.after(100, self.waitPlayerMove)
        detect_thread = threading.Thread(target=self.waitPlayerMove)
        detect_thread.setDaemon(True)
        detect_thread.start()

    def waitPlayerMove(self):
        """
        Detect player's move and show in label, then check the game
        """
        self.ctr.game.detectPlayerMove()
        self.text.set(self.ctr.game.player_move)
        self.after(2000, self.checkValid_P)

    def checkValid_P(self):
        """
        Check whether game is over/promotion/player error, if not, engine moves; contain Frame change
        """
        if self.ctr.game.over:
            self.ctr.winner.set(self.ctr.game.winner)
            self.ctr.showFrame(GameOverPage)
        elif self.ctr.game.board.promo:
            self.ctr.showFrame(ChoosePromotionPage)
        elif self.ctr.game.player_move_error:
            if self.ctr.error_cnt > 2:
                self.ctr.game.current = self.ctr.game.previous

                self.ctr.showFrame(UpdatePreviousPage)
            else:
                self.ctr.game.current = self.ctr.game.previous
                self.ctr.showFrame(PlayerMoveErrorPage)
        else:
            self.ctr.move.set(self.ctr.game.chess_engine.getEngineMove())
            self.ctr.showFrame(EngineMovePage)


class EngineMovePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        engine_move_label = tk.Label(self, text="Engine Move:", fg="red", font=MED_FONT)
        engine_move_label.pack(pady=80)

        move_label = tk.Label(self, textvariable=controller.move, fg="red", font=LARGE_FONT)
        move_label.pack(pady=50)

        self.ctr = controller

    def run(self):
        self.after(100, self.engineCheckBoard)
        # detect_thread = threading.Thread(target=self.engineCheckBoard)
        # detect_thread.setDaemon(True)
        # detect_thread.start()

    def engineCheckBoard(self):
        self.ctr.game.moveChess()
        time.sleep(0.5)
        self.ctr.game.updateCurrent()
        #        self.ctr.game.checkEngineMove()  # Involving Game.boardMatchError

        self.after(100, self.checkValid_E)

    def checkValid_E(self):

        if self.ctr.game.board_match_error:
            self.ctr.game.current = self.ctr.game.previous
            self.ctr.showFrame(BoardMatchErrorPage)
        else:
            self.ctr.game.engineMove()
            if self.ctr.game.over:
                self.ctr.winner.set(self.ctr.game.winner)
                self.ctr.showFrame(GameOverPage)
            elif self.ctr.game.is_check:
                self.ctr.showFrame(InCheckPage)
            else:
                self.ctr.showFrame(PlayerMovePage)


class ConfirmPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        confirm_label = tk.Label(self, text="Are you sure to RESIGN?", font=LARGE_FONT)
        confirm_label.pack(pady=50)

        yes_button = tk.Button(self, text="Yes, resign", font=MED_FONT,
                               command=lambda: controller.showFrame(GameOverPage))
        yes_button.pack(pady=80)
        no_button = tk.Button(self, text="No, continue", font=MED_FONT,
                              command=lambda: controller.showFrame(PlayerMovePage))
        no_button.pack(pady=50)


class GameOverPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        over_label = tk.Label(self, text="Game over!", font=LARGE_FONT)
        over_label.pack(pady=50)
        winner_label = tk.Label(self, textvariable=controller.winner, font=LARGE_FONT)
        winner_label.pack(pady=50)

        quit_button = tk.Button(self, text="Quit", font=MED_FONT,
                                command=lambda: controller.destroyFrame())
        quit_button.pack(pady=80)


class ChoosePromotionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        choose_label = tk.Label(self, text="Choose your promotion", font=LARGE_FONT)
        choose_label.pack(pady=50)

        queen_button = tk.Button(self, text="Queen(Q)",
                                 command=lambda: [self.setQueen(controller)])
        rook_button = tk.Button(self, text="Rook(R)",
                                command=lambda: [self.setRook(controller)])
        bishop_button = tk.Button(self, text="Bishop(B)",
                                  command=lambda: [self.setBishop(controller)])
        knight_button = tk.Button(self, text="Knight(N)",
                                  command=lambda: [self.setKnight(controller)])
        queen_button.pack(pady=20)
        rook_button.pack(pady=20)
        bishop_button.pack(pady=20)
        knight_button.pack(pady=20)

    @staticmethod
    def setQueen(controller):

        controller.game.board.promotion = 'q'
        controller.game.board.move = controller.game.board.move + 'q'
        controller.game.playerPromotion(controller.game.board.move)

        if controller.game.player_move_error:
            controller.game.current = controller.game.previous
            controller.showFrame(PlayerMoveErrorPage)
        else:
            controller.move.set(controller.game.chess_engine.getEngineMove())
            controller.showFrame(EngineMovePage)

    @staticmethod
    def setRook(controller):

        controller.game.board.promotion = 'r'
        controller.game.board.move = controller.game.board.move + 'r'
        controller.game.playerPromotion(controller.game.board.move)

        if controller.game.player_move_error:
            controller.game.current = controller.game.previous
            controller.showFrame(PlayerMoveErrorPage)
        else:
            controller.move.set(controller.game.chess_engine.getEngineMove())
            controller.showFrame(EngineMovePage)

    @staticmethod
    def setBishop(controller):

        controller.game.board.promotion = 'b'
        controller.game.board.move = controller.game.board.move + 'b'
        controller.game.playerPromotion(controller.game.board.move)

        if controller.game.player_move_error:
            controller.game.current = controller.game.previous
            controller.showFrame(PlayerMoveErrorPage)
        else:
            controller.move.set(controller.game.chess_engine.getEngineMove())
            controller.showFrame(EngineMovePage)

    @staticmethod
    def setKnight(controller):

        controller.game.board.promotion = 'n'
        controller.game.board.move = controller.game.board.move + 'n'
        controller.game.playerPromotion(controller.game.board.move)

        if controller.game.player_move_error:
            controller.game.current = controller.game.previous
            controller.showFrame(PlayerMoveErrorPage)
        else:
            controller.move.set(controller.game.chess_engine.getEngineMove())
            controller.showFrame(EngineMovePage)


class PlayerMoveErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        error_label = tk.Label(self, text="Error! Invalid move!\nMay be caused by camera, retry in", font=LARGE_FONT)
        error_label.pack(pady=50)
        self.countdown_label = tk.Label(self, text="5 s", font=SMALL_FONT)
        self.countdown_label.pack(pady=100)

        self.ctr = controller

    def run(self):
        self.ctr.error_cnt += 1
        self.countdown_label["text"] = "5 s"
        self.after(1000, self.countdown, 5)

    def countdown(self, n):
        n -= 1
        clock = self.after(1000, self.countdown, n)

        if n != 0:
            self.countdown_label["text"] = str(n) + " s"

        else:
            self.after_cancel(clock)
            self.countdown_label["text"] = "0"
            self.ctr.showFrame(PlayerMovePage)


class InCheckPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        check_label = tk.Label(self, text="You are in check!\nContinue in", font=LARGE_FONT, fg="red")
        check_label.pack(pady=50)
        self.countdown_label = tk.Label(self, text="5 s", font=SMALL_FONT)
        self.countdown_label.pack(pady=100)

        self.ctr = controller

    def run(self):
        self.countdown_label["text"] = "5 s"
        self.after(1000, self.countdown, 5)

    def countdown(self, n):
        n -= 1
        clock = self.after(1000, self.countdown, n)

        if n != 0:
            self.countdown_label["text"] = str(n) + " s"

        else:
            self.after_cancel(clock)
            self.countdown_label["text"] = "0"
            self.ctr.showFrame(PlayerMovePage)


class BoardMatchErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        match_error_label = tk.Label(self, text="Board match error!\nMay be caused by camera, retry in",
                                     font=LARGE_FONT)
        match_error_label.pack(pady=50)

        self.countdown_label = tk.Label(self, text="5 s", font=SMALL_FONT)
        self.countdown_label.pack(pady=100)

        self.ctr = controller

    def run(self):
        self.countdown_label["text"] = "5 s"
        self.after(1000, self.countdown, 5)

    def countdown(self, n):
        n -= 1
        clock = self.after(1000, self.countdown, n)

        if n != 0:
            self.countdown_label["text"] = str(n) + " s"

        else:
            self.after_cancel(clock)
            self.countdown_label["text"] = "0"
            self.ctr.showFrame(EngineMovePage)


class UpdatePreviousPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        error_label = tk.Label(self, text="Sorry for another error", fg="red", font=LARGE_FONT)
        error_label.pack(pady=50)
        suggest_label = tk.Label(self, text="You can NOW reset your latest move, and press:", font=MED_FONT)
        suggest_label.pack(pady=80)

        adjust_button = tk.Button(self, text="Let camera take a new image", font=MED_FONT,
                                  command=lambda: [controller.game.updatePrevious(),
                                                   controller.showFrame(PlayerMovePage)])
        adjust_button.pack(pady=40)


# Start chess game
app = Application()
app.title("Arm Chess")
wnd_w = app.winfo_screenwidth()
wnd_h = app.winfo_screenheight()
app.geometry("%dx%d" % (wnd_w, wnd_h))
app.mainloop()
