import random
import chess
import chess.engine
import numpy 
import tensorflow as tf
from keras import models
import os
Boardsnaps = []
Boardscores = []
board = chess.Board()
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


model = ""
def model_set(user):
    global model
    model = models.load_model(f'./models/{user}')

model_set("TICO")


@tf.function #This line creates an optimized graph temporarily in memory to quickly make predictions
def get_score(x):
    return model(x)





def miniMax(user,board, depth, alpha, beta, maxscorer):
    if depth == 0 or board.is_game_over():
        x = ConvertToAIboard(board) #Turns the board object into 2d array of arrays of 1s and 0s
        x = x.reshape(1,14,8,8) #Adds an extra dimension to the now array of arrays so it is like an item in a list with only one item
        return get_score(x) 

    child_nodes = list(board.legal_moves)

    if maxscorer == False: #If we want the best move for black
        worstScore = numpy.inf #The worst score is infinity
        for child in child_nodes:
            board.push(child) #Play the first move
            position_evaluation = float(miniMax(user,board,depth-1,alpha, beta, True)[0]) #Get the score at the position at the end of the tree
            board.pop() #Restore the board to before playing the move
            if position_evaluation < worstScore: #Replace the worst score as you go along to get the lowest possible score
                worstScore = position_evaluation
                best_move = child
            beta = min(beta,position_evaluation) #Pruning off the section of the tree which the oppononet is not likely to go down
            if beta <= alpha:
                break
        return worstScore, best_move
    elif maxscorer == True: #If we want the best move for white
        bestScore = -numpy.inf #The worst score is negative infinity
        for child in child_nodes:
            board.push(child)
            position_evaluation = float(miniMax(user,board,depth-1,alpha, beta, False)[0]) #Get the score at the position at the end of the tree
            board.pop() #Restore the board to before playing the move
            if position_evaluation > bestScore: #Replace the worst score as you go along to get the highest possible score
                bestScore = position_evaluation
                best_move = child
            alpha = max(alpha,position_evaluation)#Pruning off the section of the tree which the oppononet is not likely to go down
            if beta <= alpha:
                break
        return bestScore, best_move






# black win
# board.push_san("f2f4")
# board.push_san("e7e5")
# board.push_san("g2g4")
# board.push_san("d8h4")
# print(board.outcome().winner)

#white win
# board.push_san("e2e4")
# board.push_san("g7g5")
# board.push_san("f1c4")
# board.push_san("f7f5")
# board.push_san("d1h5")
# print(board.outcome().winner)



# AImove = miniMax("TICO",board, 2, -numpy.inf, numpy.inf, False)

# print(AImove)


