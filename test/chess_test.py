import chess.engine

engine = chess.engine.SimpleEngine.popen_uci('../CVChess/Stockfish-sf_15/src/stockfish')

board = chess.Board()
print(board)
while not board.is_game_over():
    move = input("Your move:\n")
    uci_move = chess.Move.from_uci(move)
    board.push(uci_move)
    print(board)
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(result.move)
    print(board.is_capture(result.move))
    board.push(result.move)
    print(board)

engine.quit()
