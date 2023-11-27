
from django.shortcuts import render
from django.http import  JsonResponse
import chess
import chess.engine
import numpy
import tensorflow as tf
from keras import models


Boardsnaps = []
Boardscores = []
board = chess.Board()
model = ""
User = ""



def model_set(user):
    global model
    model = models.load_model(f'./models/{user}')

def userSet(user):
    global User
    User = user


@tf.function #This line creates an optimized graph temporarily in memory to quickly make predictions
def get_score(x):
    return model(x)

def SaveBoardData(Boardsnaps,Boardscores):
    numpy.save("Boards.npy",Boardsnaps, True)
    numpy.save("Scores.npy",Boardscores, True)



def SaveBoard(board): #Creates and stores a picture of the chess board in this instant and records the score as well.
        AIboard = ConvertToAIboard(board)
        Score = getScore(board,not(board.turn))
        Boardsnaps.append(AIboard)
        Boardscores.append(Score)
        SaveBoardData(Boardsnaps,Boardscores)


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
        AIboard[0][position[0]][position[1]] = 1 #The first coordinate is the number of the array (out of 14) the second coordinate and the other two are x and y coordinates respectively
    for index in board.pieces(pawn_number, False): #First the indexes of all the white pawns are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8)) #Then the indexes of all the black pieces are added (from blacks perspective)
        AIboard[1][position[0]][position[1]] = 1


    for index in board.pieces(knight_number, True): #Thirdly the indexes of all the white knights are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[2][position[0]][position[1]] = 1
    for index in board.pieces(knight_number, False):#Fourthly the indexes of all the black knights are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[3][position[0]][position[1]] = 1


    for index in board.pieces(bishop_number, True):#Fifthly the indexes of all the white bishops are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[4][position[0]][position[1]] = 1
    for index in board.pieces(bishop_number, False):#sixthly the indexes of all the black bishops are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[5][position[0]][position[1]] = 1


    for index in board.pieces(rook_number, True):#seventhly the indexes of all the white rooks are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[6][position[0]][position[1]] = 1
    for index in board.pieces(rook_number, False):#eightly the indexes of all the black rooks are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[7][position[0]][position[1]] = 1


    for index in board.pieces(queen_number, True):#ninthly the indexes of all the white queens are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[8][position[0]][position[1]] = 1
    for index in board.pieces(queen_number, False):#tenthly the indexes of all the black queens are added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[9][position[0]][position[1]] = 1


    for index in board.pieces(king_number, True):#eleventhly the indexes of the white king is added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[10][position[0]][position[1]] = 1
    for index in board.pieces(king_number, False):#twelvethly the indexes of the black king is added to the numpy array: AIboard (from blacks perspective)
        position = numpy.unravel_index(index, (8, 8))
        AIboard[11][position[0]][position[1]] = 1



    #The pairs of for loops create 2, two dimensional numpy arrays with ones representing the case where a piece of the 
    #corresponding number and color is positioned on it




    

    RealTurn = board.turn#The current players turn is saved so the board can be restored to it.
    board.turn = chess.WHITE#The board is viewed from whites perspective
    for move in board.generate_legal_captures():#This method returns all the moves that result in white capturing a piece e.g: Move.from_uci('d4c5')
        letter = chess.square_name(move.to_square) #This function call converts the square index of a square such as 28 to its name; which for '28' would be 'e4'
        x = 8 - int(letter[1])
        if letter[0] == "a":
            y = 0
        if letter[0] == "b":
            y = 1
        if letter[0] == "c":
            y = 2
        if letter[0] == "d":
            y = 3
        if letter[0] == "e":
            y = 4
        if letter[0] == "f":
            y = 5
        if letter[0] == "g":
            y = 6
        if letter[0] == "h":
            y = 7
        AIboard[12][x][y] = 1

    board.turn = chess.BLACK#The board is viewed from blacks perspective
    for move in board.generate_legal_captures():
        letter = chess.square_name(move.to_square) #the .to_square method is called to just get the target square ("c5") in square index form: 34
        x = 8 - int(letter[1])
        if letter[0] == "a":
            y = 0
        if letter[0] == "b":
            y = 1
        if letter[0] == "c":
            y = 2
        if letter[0] == "d":
            y = 3
        if letter[0] == "e":
            y = 4
        if letter[0] == "f":
            y = 5
        if letter[0] == "g":
            y = 6
        if letter[0] == "h":
            y = 7
        AIboard[13][x][y] = 1

    board.turn = RealTurn

    #The above chunk of code turns all the squares that black and white can capture a piece on and converts it into into a square index
    #The chunck of code saves the current player turn in a temporay variable to restore to once its simulated the board from the perspective of both players
    #the x coordinate is transformed so that it is from the perspective of the attacking side where the attacked piece is

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



def miniMax(board, depth, alpha, beta, maxscorer):
    if depth == 0 or board.is_game_over():
        x = ConvertToAIboard(board) #Turns the board object into 2d array of arrays of 1s and 0s
        x = x.reshape(1,14,8,8) #Adds an extra dimension to the now array of arrays so it is like an item in a list with only one item
        return get_score(x) 

    child_nodes = list(board.legal_moves)

    if maxscorer == False: #If we want the best move for black
        worstScore = numpy.inf #The worst score is infinity
        for child in child_nodes:
            board.push(child) #Play the first move
            position_evaluation = float(miniMax(board,depth-1,alpha, beta, True)[0]) #Get the score at the position at the end of the tree
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
            position_evaluation = float(miniMax(board,depth-1,alpha, beta, False)[0]) #Get the score at the position at the end of the tree
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

    x_test = numpy.load("testboards.npy")
    y_test = numpy.load("testscores.npy")
    y_test = numpy.asarray(y_test / abs(y_test)/2 +0.5 , dtype=numpy.float32) # normalization (0 - 1)

    model.fit(x,y,epochs=100)
    results = model.evaluate(x_test, y_test, batch_size=128)
    relative = results[1] *100
    User.updateRelative(relative)
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
    global board
    temp = request.GET.get('hide')
    legalEnPassant =  board.has_legal_en_passant()
    whiteKingSide = board.has_kingside_castling_rights(True)
    whiteQueenSide = board.has_queenside_castling_rights(True)
    blackQueenSide = board.has_queenside_castling_rights(False)
    blackKingSide = board.has_kingside_castling_rights(False)
    
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
    if User == "":
        return render(request, 'mainpage.html')
    else:
        return render(request, 'mainpage.html',{'Username' : User.getUsername()})




def AiMove(request):
    # global count
    global board
    temp = request.GET.get('stuff')
    legalEnPassant =  board.has_legal_en_passant()
    whiteKingSide = board.has_kingside_castling_rights(True)
    whiteQueenSide = board.has_queenside_castling_rights(True)
    blackQueenSide = board.has_queenside_castling_rights(False)
    blackKingSide = board.has_kingside_castling_rights(False)
    moveAI = ""
    

    try: #This is my actual AI code
        moveAI = (miniMax(board, 3, -numpy.inf, numpy.inf, False)[1])
        board.push(moveAI)
        SaveBoard(board)
    except Exception as e: #If the game is over and the AI lost then no AI move should be returned
        pass
    moveAI = str(moveAI)
    gameOver = board.is_game_over()


    return JsonResponse({"legalEnPassant": legalEnPassant,
    "whiteKingSide": whiteKingSide,
    "whiteQueenSide": whiteQueenSide,
    "blackQueenSide": blackQueenSide,
    "blackKingSide": blackKingSide,
    "moveAI": moveAI,
    "gameOver":gameOver }, status = 200)