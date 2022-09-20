
import chess
import chess.engine

import tensorflow as tf
from tensorflow import keras
from keras import layers, models
import numpy 

Boardsnaps = []
Boardscores = []
board = chess.Board()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Tells program to ignore an unimportant warning


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
  letter = chess.square_name(square) #This function call converts the square index of a square such as 28 to its name; which for '28' would be 'e4'
  return 8 - int(letter[1]), letterToCoordinate[letter[0]] #This part takes that name, e.g. 'e4' and convert this position to its coordinate of 4 4 using the letterToCoordinate dictionary to convert the letter


def ConvertToAIboard(board):
    #This program turns the chess board into something the AI can analyse better
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



    #The pairs of for loops create 2, two dimensional numpy arrays with ones representing the case where a piece of the 
    #corresponding number and color is positioned on it




    RealTurn = board.turn
    board.turn = chess.WHITE
    for move in board.generate_legal_captures():
        y , x = coordinateToIndex(move.to_square)
        AIboard[12][y][x] = 1

    board.turn = chess.BLACK
    for move in board.generate_legal_captures():
        y , x = coordinateToIndex(move.to_square)
        AIboard[13][y][x] = 1

    board.turn = RealTurn

    #The above chunk of code turns all the squares that black and white can capture a piece on and converts it into into a square index
    #The chunck of code saves the current player turn in a temporray variable to retore to once its simulated the board from the perspective of both players


    return(AIboard)

def getScore():
    global board
    with chess.engine.SimpleEngine.popen_uci("templates\stockfish.exe") as stockfish: #Calling a well known chess AI to give an estimated board score at a certain position for a given board position
        info = stockfish.analyse(board, chess.engine.Limit(time=0.1))
        if info["score"].is_mate():
            if info["score"].white().mate() == 1:
                return 1000
            if info["score"].black().mate() == 1:
                return -1000
            if board.outcome().winner == True:
                return 10000
            if board.outcome().winner == False:
                return -10000
        else:
            return info["score"].white().score()


# #White win
# board.push_san("e2e4")
# print(getScore())

# board.push_san("g7g5")
# print(getScore())

# board.push_san("f1c4")
# print(getScore())

# board.push_san("f7f5")
# print(getScore())

# board.push_san("d1h5")
# print(getScore())








#Black win
# board.push_san("f2f4")
# print(getScore())

# board.push_san("e7e5")
# print(getScore())

# board.push_san("g2g4")
# print(getScore())

# board.push_san("d8h4")
# print(getScore())




def build_model(conv_size, conv_depth):
  board3d = layers.Input(shape=(14, 8, 8))

  # adding the convolutional layers
  x = board3d
  for _ in range(conv_depth):
    x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu', data_format='channels_first')(x)
  x = layers.Flatten()(x)
  x = layers.Dense(64, 'relu')(x)
  x = layers.Dense(1, 'sigmoid')(x)

  return models.Model(inputs=board3d, outputs=x)




board = chess.Board()
board.push_san("e4")
AIboard = ConvertToAIboard(board)

x = numpy.load("Boards.npy")

y = numpy.load("Scores.npy")
y = numpy.asarray(y / abs(y).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)
print(y)
x = x.reshape(5,14,8,8)

model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape = (14,8,8)), 
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                    tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)])
model.compile(optimizer=tf.keras.optimizers.Adam(), loss= 'sparse_categorical_crossentropy')
model.fit(x,y,epochs=10)
m = AIboard.reshape(1,14,8,8)
print(model.predict(x))