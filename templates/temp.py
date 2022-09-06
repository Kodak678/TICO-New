import chess
import numpy
board  = chess.Board()

# moves = []
# for move in board.legal_moves:
#     moves.append(str(move))

# print(moves)




AIboard = numpy.zeros((14, 8, 8), dtype=numpy.int8)
pawn_number = 1
knight_number = 2
bishop_number = 3
rook_number = 4
queen_number = 5
king_number = 6

#unravel_index converts an index such as 9 into its corresponding co ordinate for an array of given dimensions.
#for example: in an 8 by 8 dimensional array: the co ordinates corresponding to the index 9 would be (1,1)
#The index (1,1) was calculated by doing 1 x 8 + 1 to get 9




for index in board.pieces(pawn_number, True):
    position = numpy.unravel_index(index, (8, 8))  #In a board of 64, each coordinate is represented by an index numberered from 0 to 63, in order to convert this index to a coordinate: I have unravelled it
    AIboard[pawn_number - 1][position[0]][position[1]] = 1 #The first coordinate is the number of the array (out of 12) the second coordinate and the other two are y and x coordinates respectively
for index in board.pieces(pawn_number, False): #First the indexes of all the white pieces of the piece number are added to the numpy array: AIboard
    position = numpy.unravel_index(index, (8, 8))
    AIboard[pawn_number][position[0]][position[1]] = 1


for index in board.pieces(knight_number, True):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[knight_number][position[0]][position[1]] = 1
for index in board.pieces(knight_number, False):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[knight_number + 1][position[0]][position[1]] = 1


for index in board.pieces(bishop_number, True):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[bishop_number + 1][position[0]][position[1]] = 1
for index in board.pieces(bishop_number, False):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[bishop_number + 2][position[0]][position[1]] = 1


for index in board.pieces(rook_number, True):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[rook_number + 2][position[0]][position[1]] = 1
for index in board.pieces(rook_number, False):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[rook_number + 3][position[0]][position[1]] = 1


for index in board.pieces(queen_number, True):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[queen_number + 3][position[0]][position[1]] = 1
for index in board.pieces(queen_number, False):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[queen_number + 4][position[0]][position[1]] = 1


for index in board.pieces(king_number, True):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[king_number + 4][position[0]][position[1]] = 1
for index in board.pieces(king_number, False):
    position = numpy.unravel_index(index, (8, 8))
    AIboard[king_number + 5][position[0]][position[1]] = 1



letterToCoordinate = {
  'a': 0,
  'b': 1,
  'c': 2,
  'd': 3,
  'e': 4,
  'f': 5,
  'g': 6,
  'h': 7
}



def coordinateToIndex(square):
  letter = chess.square_name(square)
  return 8 - int(letter[1]), letterToCoordinate[letter[0]]

board.push_san("e2e4")
board.push_san("d7d5")
print(board)


trial = numpy.zeros((2, 8, 8), dtype=numpy.int8)

RealTurn = board.turn
board.turn = chess.WHITE
for move in board.generate_legal_captures():
  y , x = coordinateToIndex(move.to_square)
  trial[0][y][x] = 1

board.turn = chess.BLACK
for move in board.generate_legal_captures():
  y , x = coordinateToIndex(move.to_square)
  trial[1][y][x] = 1

board.turn = RealTurn



print(trial)


