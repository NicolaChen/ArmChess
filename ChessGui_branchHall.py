import threading
import time
import tkinter as tk
from tkinter import *

from HallEffectBoard.Game import Game

LARGE_FONT = ("system", 80)
MED_FONT = ("system", 50)
SMALL_FONT = ("system", 30)


def enableButton(button):
    button['state'] = tk.NORMAL


def disableButton(button):
    button['state'] = tk.DISABLED


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

        for F in (StartGamePage, SetBoardPage, ChooseDifficultyPage, ChooseColorPage, PlayerMovePage,
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
        self.game.chess_engine.engine.close()
        app.destroy()


class StartGamePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title_label = tk.Label(self, text="ArmChess with Hall Effect Board", fg="blue", font=LARGE_FONT)
        title_label.pack(anchor='center', pady=50)

        start_button = tk.Button(self, text="Start Chess Game", fg="green", font=MED_FONT,
                                 command=lambda: [disableButton(start_button),
                                                  controller.showFrame(ChooseColorPage), controller.game.setUp()])
        start_button.pack(anchor='center', pady=50)


class ChooseColorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        color_label = tk.Label(self, text="Choose your side and\nput the board to right direction", font=LARGE_FONT)
        color_label.pack(pady=20)

        white_button = tk.Button(self, text="White(Blue)", font=MED_FONT, fg="blue",
                                 command=lambda: [controller.showFrame(SetBoardPage),
                                                  controller.game.setArmSide('Black')])
        white_button.pack(pady=30)
        black_button = tk.Button(self, text="Black(Red)", font=MED_FONT, fg="red",
                                 command=lambda: [controller.showFrame(SetBoardPage),
                                                  controller.game.setArmSide('White')])
        black_button.pack(pady=20)


class SetBoardPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        set_board_label = tk.Label(self, text="Set the board", font=LARGE_FONT)
        set_board_label.pack(pady=30)

        self.ctr = controller

    def run(self):
        is_set = False
        while not is_set:
            is_set = self.ctr.game.isBoardSet()
        self.ctr.showFrame(ChooseDifficultyPage)


class ChooseDifficultyPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        choose_difficulty_label = tk.Label(self, text="Choose difficulty", font=LARGE_FONT)
        choose_difficulty_label.pack(pady=5)

        tk.Button(self, text="Easy", font=SMALL_FONT,
                  command=lambda: [self.setEasy(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=5)
        tk.Button(self, text="Intermediate", font=SMALL_FONT, fg="green",
                  command=lambda: [self.setIntermediate(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=5)
        tk.Button(self, text="Hard", font=SMALL_FONT, fg="blue",
                  command=lambda: [self.setHard(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=5)
        tk.Button(self, text="Extreme", font=SMALL_FONT, fg="purple",
                  command=lambda: [self.setExtreme(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=5)
        tk.Button(self, text="Master", font=SMALL_FONT, fg="red",
                  command=lambda: [self.setMaster(controller),
                                   controller.showFrame(PlayerMovePage) if controller.game.arm_side == 'Black' else
                                   (controller.move.set(controller.game.chess_engine.getEngineMove()),
                                    controller.showFrame(EngineMovePage))]).pack(pady=5)

    @staticmethod
    def setEasy(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 0, "Hash": 64})
        controller.game.chess_engine.time = 1

    @staticmethod
    def setIntermediate(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 5, "Hash": 128})
        controller.game.chess_engine.time = 3

    @staticmethod
    def setHard(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 10, "Hash": 512})
        controller.game.chess_engine.time = 5

    @staticmethod
    def setExtreme(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 15, "Hash": 1024})
        controller.game.chess_engine.time = 10

    @staticmethod
    def setMaster(controller):
        controller.game.chess_engine.engine.configure({"Skill Level": 20, "Hash": 2048})
        controller.game.chess_engine.time = 20


class PlayerMovePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        start_label = tk.Label(self, text="Make your move", fg="green", font=LARGE_FONT)
        start_label.pack(pady=0)

        resign_button = tk.Button(self, text="Resign", font=SMALL_FONT,
                                  command=lambda: [self.stopThread(), controller.showFrame(ConfirmPage)])
        resign_button.pack(pady=5)

        show_move_label = tk.Label(self, text="Detect your move is:", font=MED_FONT)
        show_move_label.pack(pady=5)

        self.text = StringVar()
        player_move_label = tk.Label(self, textvariable=self.text, font=SMALL_FONT, fg="green")
        player_move_label.pack(pady=5)

        # move_input_label = tk.Label(self, text="Or you can manually input your move in UCI: ", font=SMALL_FONT)
        # move_input_label.pack(pady=5)
        #
        # self.input_text = tk.Text(self, width=5, height=2)
        # self.input_text.pack(pady=5)
        #
        # self.get_input_button = tk.Button(self, text="Insert", font=SMALL_FONT,
        #                                   command=lambda: [disableButton(self.get_input_button),
        #                                                    self.stopThread(), self.insertText()])
        # self.get_input_button.pack(pady=5)

        self.ctr = controller
        self.detect_thread = None

    def stopThread(self):
        self.ctr.game.stop_detect_flag = True

    # def insertText(self):
    #     insert_text = self.input_text.get("1.0", "end-1c")
    #     self.input_text.delete("1.0", "end")
    #     self.ctr.game.playerMove(insert_text)
    #     self.text.set(self.ctr.game.player_move)
    #     self.after(2000, self.checkValid_P)

    def run(self):
        # enableButton(self.get_input_button)
        self.ctr.game.stop_detect_flag = False
        self.text.set("Waiting for your move ...")
        self.detect_thread = threading.Thread(target=self.waitPlayerMove)
        self.detect_thread.setDaemon(True)
        self.detect_thread.start()

    def waitPlayerMove(self):
        """
        Detect player's move and show in label, then check the game
        """
        res = self.ctr.game.detectPlayerMove()
        if res == 0:
            return 0
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
            self.ctr.showFrame(PlayerMoveErrorPage)
        else:
            self.ctr.move.set(self.ctr.game.chess_engine.getEngineMove())
            self.ctr.showFrame(EngineMovePage)


class EngineMovePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        engine_move_label = tk.Label(self, text="Engine Move:", fg="red", font=MED_FONT)
        engine_move_label.pack(pady=20)

        move_label = tk.Label(self, textvariable=controller.move, fg="red", font=LARGE_FONT)
        move_label.pack(pady=50)

        self.ctr = controller

    def run(self):
        # self.after(100, self.engineCheckBoard)
        detect_thread = threading.Thread(target=self.engineCheckBoard)
        detect_thread.setDaemon(True)
        detect_thread.start()

    def engineCheckBoard(self):
        self.ctr.game.moveChess()
        time.sleep(0.5)
        # self.ctr.game.checkEngineMove()  # Involving Game.boardMatchError

        self.after(100, self.checkValid_E)

    def checkValid_E(self):

        if self.ctr.game.board_match_error:
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
        confirm_label = tk.Label(self, text="Sure to resign?", font=LARGE_FONT)
        confirm_label.pack(pady=20)

        yes_button = tk.Button(self, text="Yes, resign", font=MED_FONT,
                               command=lambda: controller.showFrame(GameOverPage))
        yes_button.pack(pady=30)
        no_button = tk.Button(self, text="No, continue", font=MED_FONT,
                              command=lambda: controller.showFrame(PlayerMovePage))
        no_button.pack(pady=20)


class GameOverPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        over_label = tk.Label(self, text="Game over!", font=LARGE_FONT)
        over_label.pack(pady=20)
        winner_label = tk.Label(self, textvariable=controller.winner, font=LARGE_FONT)
        winner_label.pack(pady=20)

        quit_button = tk.Button(self, text="Quit", font=MED_FONT,
                                command=lambda: controller.destroyFrame())
        quit_button.pack(pady=30)


class ChoosePromotionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        choose_label = tk.Label(self, text="Choose your promotion", font=LARGE_FONT)
        choose_label.pack(pady=5)

        queen_button = tk.Button(self, text="Queen(Q)",
                                 command=lambda: [self.setQueen(controller)])
        rook_button = tk.Button(self, text="Rook(R)",
                                command=lambda: [self.setRook(controller)])
        bishop_button = tk.Button(self, text="Bishop(B)",
                                  command=lambda: [self.setBishop(controller)])
        knight_button = tk.Button(self, text="Knight(N)",
                                  command=lambda: [self.setKnight(controller)])
        queen_button.pack(pady=10)
        rook_button.pack(pady=10)
        bishop_button.pack(pady=10)
        knight_button.pack(pady=10)

    @staticmethod
    def setQueen(controller):

        # controller.game.board.promotion = 'q'
        # controller.game.board.move = controller.game.board.move + 'q'
        controller.game.playerPromotion(controller.game.player_move)  # TODO: Adjust promotion func here and in Game

        if controller.game.player_move_error:
            controller.showFrame(PlayerMoveErrorPage)
        else:
            controller.move.set(controller.game.chess_engine.getEngineMove())
            controller.showFrame(EngineMovePage)

    @staticmethod
    def setRook(controller):

        # controller.game.board.promotion = 'r'
        # controller.game.board.move = controller.game.board.move + 'r'
        controller.game.playerPromotion(controller.game.player_move)

        if controller.game.player_move_error:
            controller.showFrame(PlayerMoveErrorPage)
        else:
            controller.move.set(controller.game.chess_engine.getEngineMove())
            controller.showFrame(EngineMovePage)

    @staticmethod
    def setBishop(controller):

        # controller.game.board.promotion = 'b'
        # controller.game.board.move = controller.game.board.move + 'b'
        controller.game.playerPromotion(controller.game.player_move)

        if controller.game.player_move_error:
            controller.showFrame(PlayerMoveErrorPage)
        else:
            controller.move.set(controller.game.chess_engine.getEngineMove())
            controller.showFrame(EngineMovePage)

    @staticmethod
    def setKnight(controller):

        # controller.game.board.promotion = 'n'
        # controller.game.board.move = controller.game.board.move + 'n'
        controller.game.playerPromotion(controller.game.player_move)

        if controller.game.player_move_error:
            controller.showFrame(PlayerMoveErrorPage)
        else:
            controller.move.set(controller.game.chess_engine.getEngineMove())
            controller.showFrame(EngineMovePage)


class PlayerMoveErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        error_label = tk.Label(self, text="Error! Invalid move!\nReset now and then retry in",
                               fg="red", font=MED_FONT)
        error_label.pack(pady=20)
        self.countdown_label = tk.Label(self, text="5 s", font=MED_FONT)
        self.countdown_label.pack(pady=30)

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
        check_label.pack(pady=20)
        self.countdown_label = tk.Label(self, text="5 s", font=MED_FONT)
        self.countdown_label.pack(pady=30)

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

        match_error_label = tk.Label(self, text="Board match error!\nArm will retry in",
                                     font=LARGE_FONT)
        match_error_label.pack(pady=20)

        self.countdown_label = tk.Label(self, text="5 s", font=MED_FONT)
        self.countdown_label.pack(pady=30)

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


# Start chess game
app = Application()
app.title("Arm Chess")
wnd_w = app.winfo_screenwidth()
wnd_h = app.winfo_screenheight()
app.geometry("%dx%d" % (wnd_w, wnd_h))
app.protocol("WM_DELETE_WINDOW", app.destroyFrame)
app.mainloop()
