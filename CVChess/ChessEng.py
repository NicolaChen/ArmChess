import chess
import chess.engine


class ChessEng:

    def __init__(self):

        self.engBoard = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("CVChess/Stockfish-sf_15/src/stockfish")
        self.time = 0.1
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

    def feedToEngine(self):

        result = self.engine.play(self.engBoard, chess.engine.Limit(time=self.time))
        best_move = result.move
        self.engBoard.push(best_move)

        f = open("ChessRecord.txt", "a+")
        f.write(best_move.uci() + "\r\n")
        f.close()

        print(self.engBoard)
        return best_move
