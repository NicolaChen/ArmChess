import chess.engine

engine = chess.engine.SimpleEngine.popen_uci('../CVChess/Stockfish-sf_15/src/stockfish')

board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(board.san(chess.Move.from_uci(str(result.move))))
    print(board.is_en_passant(chess.Move.from_uci(str(result.move))))
    print(board.is_capture(chess.Move.from_uci(str(result.move))))
    board.push(result.move)

engine.quit()
