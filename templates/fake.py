
import random
import chess
import chess.engine
import numpy 
import tensorflow as tf
from keras import models
import os
import sqlite3
import absl.logging
Boardsnaps = []
Boardscores = []
board = chess.Board()
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
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Tells program to ignore an unimportant warning
absl.logging.set_verbosity(absl.logging.ERROR)  #Tells program to ignore an unimportant warning




def train_model(user):
    x = numpy.load("ManyBoards.npy")
    y = numpy.load("ManyScores.npy")
    y = numpy.asarray(y / abs(y).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)
    model = models.load_model(f'./models/{user}')
    model.fit(x,y,epochs=100)
    model.save(f'./models/{user}')

def SaveBoardData(Boardsnaps,Boardscores):
    numpy.save("SumBoards.npy",Boardsnaps, True)
    numpy.save("SumScores.npy",Boardscores, True)

def getScore(board,side):
    with chess.engine.SimpleEngine.popen_uci("templates\stockfish.exe") as stockfish: #Calling a well known chess AI to give an estimated board score at a certain position for a given board position
        info = stockfish.analyse(board, chess.engine.Limit(time=0.01))
        if info["score"] == "None":
            return 0
        if str(info["score"].relative) == "#-0" and side:
            return 100000
        if str(info["score"].relative) == "#-0"and (not(side)):
            return -100000
        if "#" in str(info["score"].relative):
            return int(str(info["score"].relative)[1:])
        else:
            return int(str(info["score"].white().score()))

def SaveBoard(board): #Creates and stores a picture of the chess board in this instant and records the score as well.
        AIboard = ConvertToAIboard(board)
        Score = getScore(board,not(board.turn))
        Boardsnaps.append(AIboard)
        Boardscores.append(Score)
        SaveBoardData(Boardsnaps,Boardscores)

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





def generate_data(): #To generate data for my heuristic model to learn from.
    temp_board = chess.Board()

    while not(temp_board.is_game_over()):
        child_nodes = list(temp_board.legal_moves)
        move = random.choice(child_nodes)
        temp_board.push(move)
        SaveBoard(temp_board)

def create_model():
    model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape = (14,8,8)), 
                                        tf.keras.layers.Dense(64, activation=tf.keras.activations.linear),    
                                        tf.keras.layers.Dense(32, activation=tf.keras.activations.linear),    
                                        tf.keras.layers.Dense(1, activation=tf.keras.activations.linear)])
    model.compile(optimizer=tf.keras.optimizers.Adam(5e-4), loss = tf.keras.losses.mean_squared_error, metrics=["accuracy"])
    return model



model = create_model()


# for i in range(0,50):  #All player's weights should be initialized with some exposure to some data    
#     generate_data()  # to create the data needed



x = numpy.load("SumBoards.npy")
y = numpy.load("SumScores.npy")

# count = 0
# for i in x:
#     count+=1
# print(count)

# count1 = 0
# for i in y:
#     count1+=1
# print(count1)

# x = numpy.load("TestBoards.npy")
# y = numpy.load("TestScores.npy")
# y = numpy.asarray(y / abs(y).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)

model.fit(x,y,epochs=100)
model.fit(x,y,epochs=100)
model.fit(x,y,epochs=100)
model.fit(x,y,epochs=100)



x_test = numpy.load("TestBoards.npy")
y_test = numpy.load("TestScores.npy")
y_test = numpy.asarray(y_test / abs(y_test).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)

results = model.evaluate(x_test, y_test, batch_size=128)
print(results)
# relative = (( 0.0006020597647875547 - results ) / 0.0006020597647875547) *100
# print(relative)


[9.614791633794084e-05, 0.001998001942411065]
[3.731828473974019e-05, 0.001998001942411065]
[2.7800646421383135e-05, 0.001998001942411065]