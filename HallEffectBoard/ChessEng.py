import chess
import chess.engine


class ChessEng:

    def __init__(self):

        self.engBoard = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("CVChess/Stockfish-sf_15/src/stockfish")
        self.time = 15
        self.engine_move = None
        print(self.engBoard)

    def updateMove(self, move):

        uci_move = chess.Move.from_uci(move)
        if uci_move not in self.engBoard.legal_moves:
            # illegal move
            return 1
        else:
            # update board
            self.engBoard.push(uci_move)
            print(self.engBoard)
            return 0

    def getEngineMove(self):

        self.engine_move = self.engine.play(self.engBoard, chess.engine.Limit(time=self.time, depth=50)).move
        return self.engine_move

    def feedToEngine(self):

        best_move = self.engine_move
        self.engBoard.push(best_move)

        f = open("ChessRecord.txt", "a+")
        f.write(best_move.uci() + "\r\n")
        f.close()

        print(self.engBoard)

    def getLegalMoves(self, pos):
        """
        根据所给移动棋子的位置，遍历全局找到该棋子合法的移动位置，返回串口输出所需的字符串
        """
        column = ["a", "b", "c", 'd', "e", "f", "g", "h"]
        row = ["1", "2", "3", "4", "5", "6", "7", "8"]
        res_str = "T" + pos + "bT"
        for c in column:
            for r in row:
                if c == pos[0] and r == pos[1]:
                    continue
                uci_move = pos + c + r
                move = chess.Move.from_uci(uci_move)
                if move in self.engBoard.legal_moves:
                    res_str += c + r + "gT"
        res_str += "endT"
        return res_str
