# moves = ['e7e6','f8e7','g8f6','e8g8'] #Castling for white and black kingside
import chess
board = chess.Board()
board.push_san("e2e3")
board.push_san("e7e6")
board.push_san("f1d3")
board.push_san("f8e7")
board.push_san("g1e2")
board.push_san("g8f6")
print(board.has_kingside_castling_rights(True))
board.push_san("e1f1")
print(board.has_kingside_castling_rights(True))
board.push_san("e8g8")