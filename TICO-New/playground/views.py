
from django.shortcuts import render
from django.http import  JsonResponse
import chess
import chess.engine
import random
import numpy
import tensorflow as tf
from keras import models
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Tells program to ignore an unimportant warning

Boardsnaps = []
Boardscores = []
board = chess.Board()
model = ""
User = ""

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

def model_set(user):
    global User, model
    model = models.load_model(f'./models/{User.getUsername()}')




@tf.function #This line creates an optimized graph temporarily in memory to quickly make predictions
def get_score(x):
    return model(x)

def SaveBoardData(Boardsnaps,Boardscores):
    numpy.save("ManyBoards.npy",Boardsnaps, True)
    numpy.save("ManyScores.npy",Boardscores, True)




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

def train_model(request):
    global User
    temp = request.GET.get('hide')
    x = numpy.load("Boards.npy")
    y = numpy.load("Scores.npy")
    y = numpy.asarray(y / abs(y).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)
    model.fit(x,y,epochs=100)
    model.save(f'./models/{User.getUsername()}')
    return JsonResponse({"trained": True},status = 200)





def isValid(move):
    global board
    try:
        board.push_san(move)
        SaveBoard(board)
        return True
    except ValueError:
        return False


def boardStates(request):
    temp = request.GET.get('hide')
    legalEnPassant =  board.has_legal_en_passant()
    whiteKingSide = bool(chess.BB_H1)
    whiteQueenSide = bool(chess.BB_A1)
    blackQueenSide = bool(chess.BB_A8)
    blackKingSide = bool(chess.BB_H8)
    return JsonResponse({"legalEnPassant": legalEnPassant,
    "whiteKingSide": whiteKingSide,
    "whiteQueenSide": whiteQueenSide,
    "blackQueenSide": blackQueenSide,
    "blackKingSide": blackKingSide},status = 200)



def resetBoard(request):
    temp = request.GET.get('hide')
    board.reset()
    return JsonResponse({"reset":True}, status = 200)

def getWinner(request):
    temp = request.GET.get('hide')
    winner = board.outcome().winner
    if winner == True:
        winner = "White Wins!"
    else:
        winner = "Black Wins!"
    return JsonResponse({"winner":winner}, status = 200)


def validMove(request):
    move = str(request.POST.get('move'))
    m = isValid(move)
    gameOver = board.is_game_over()
    return JsonResponse({
    "gameOver": gameOver,
    "valid": m }, status = 200)
    



def load_board(request):
    global User
    from users.views import LoggedInUser
    if LoggedInUser == "":
        return render(request, 'mainpage.html')
    else:
        User = LoggedInUser
        model_set(User.getUsername()) 
        return render(request, 'board.html')
    
def home(request):
    return render(request, 'mainpage.html')



# count = 0
def AiMove(request):
    global count
    temp = request.GET.get('stuff')
    legalEnPassant =  board.has_legal_en_passant()
    whiteKingSide = bool(chess.BB_H1)
    whiteQueenSide = bool(chess.BB_A1)
    blackQueenSide = bool(chess.BB_A8)
    blackKingSide = bool(chess.BB_H8)
    
    
    # moves = ['d7d5','d5c4','c4b3','b3a2','a2b1q'] #A specififc set of moves to test the AI can promote pawns as expected
    # moves = ['d7d5','d5e4','e4f3','f3g2','g2h1q'] #A specififc set of moves to test the AI can promote pawns as expected

    # moves = ['g7g5','g5g4','g4h3']  #A black side enpassant capture
    # moves = ['g7g5','g5g4','g4f3']  #A black side enpassant capture

    # moves = ['h7h6','a7a5'] #A white side enpassant capture
    # moves = ['h7h6','d7d5'] #A white side enpassant capture

    # moves = ['e7e6','f8e7','g8f6','e8g8'] #Castling for white and black kingside
    # moves = ['d7d5','c8e6','b8c6','d8d7','e8c8'] #Castling for white and black queenside

    # board.push_uci(moves[count])
    # moveAI = moves[count]
    # count += 1

    # try: #Playing against a random AI which is easy to beat for testing what happens when the player wins
    #     child_nodes = list(board.legal_moves)
    #     move = random.choice(child_nodes)
    #     board.push(move)
    #     SaveBoard(board)
    #     moveAI = str(move)
    # except IndexError: #What to do if the the game is over (AI lost) 
    #     moveAI = ""
    # gameOver = board.is_game_over()

    # try: #Playing against the most power chess AI at this time to get beaten by the AI to see what happens when the AI wins
    #     Stockfish = chess.engine.SimpleEngine.popen_uci("templates\stockfish.exe")
    #     moveAI = Stockfish.play(board,chess.engine.Limit(time=0.1))
    #     Stockfish.quit()
    #     board.push(moveAI.move)
    #     SaveBoard(board)
    #     moveAI = str(moveAI.move)
    # except AttributeError: #What to do if the the game is over (AI lost) 
    #     moveAI = ""  
    # gameOver = board.is_game_over()

    try: #This is my actual AI code
        moveAI = (miniMax("TICO",board, 2, -numpy.inf, numpy.inf, False)[1])
        board.push(moveAI)
        SaveBoard(board)
    except Exception as e: #If the game is over and the AI lost then no AI move should be returned
        moveAI = ""
    gameOver = board.is_game_over()
    moveAI = str(moveAI)


    return JsonResponse({"legalEnPassant": legalEnPassant,
    "whiteKingSide": whiteKingSide,
    "whiteQueenSide": whiteQueenSide,
    "blackQueenSide": blackQueenSide,
    "blackKingSide": blackKingSide,
    "moveAI": moveAI,
    "gameOver":gameOver }, status = 200)