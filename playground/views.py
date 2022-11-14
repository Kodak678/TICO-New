
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import chess
import chess.engine
import random
import numpy


board = chess.Board()





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
        return getScore(board,not(board.turn)) #Supplying the opposite of the board turn 

    child_nodes = list(board.legal_moves)

    if maxscorer == False:
        worstScore = numpy.inf
        for child in child_nodes:
            board.push(child)
            position_evaluation = miniMax(board,depth-1,alpha, beta, True)
            board.pop()
            if position_evaluation < worstScore:
                worstScore = position_evaluation
                best_move = child
            beta = min(beta,position_evaluation)
            if beta <= alpha:
                break
        return worstScore
    elif maxscorer == True:
        bestScore = -numpy.inf
        for child in child_nodes:
            board.push(child)
            position_evaluation = miniMax(board,depth-1,alpha, beta, False)
            board.pop()
            if position_evaluation > bestScore:
                bestScore = position_evaluation
                best_move = child
            alpha = max(alpha,position_evaluation)
            if beta <= alpha:
                break
        return bestScore









def isValid(move):
    try:
        board.push_san(move)
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
    from users import views as users
    if users.loggedInUser == "":
        return render(request, 'mainpage.html')
    else:
        return render(request, 'board.html') 
    
def home(request):
    return render(request, 'mainpage.html')


def AiMove(request):
    temp = request.GET.get('stuff')
    legalEnPassant =  board.has_legal_en_passant()
    whiteKingSide = bool(chess.BB_H1)
    whiteQueenSide = bool(chess.BB_A1)
    blackQueenSide = bool(chess.BB_A8)
    blackKingSide = bool(chess.BB_H8)
    
    try:
        child_nodes = list(board.legal_moves)
        move = random.choice(child_nodes)
        board.push(move)
        moveAI = str(move)
    except IndexError: #What to do if the the game is over (AI lost) 
        moveAI = ""
    gameOver = board.is_game_over()

    # try:
    #     Stockfish = chess.engine.SimpleEngine.popen_uci("templates\stockfish.exe")
    #     moveAI = Stockfish.play(board,chess.engine.Limit(time=0.1))
    #     Stockfish.quit()
    #     board.push(moveAI.move)
    #     moveAI = str(moveAI.move)
    # except AttributeError: #What to do if the the game is over (AI lost) 
    #     moveAI = ""  
    # gameOver = board.is_game_over()
    
    return JsonResponse({"legalEnPassant": legalEnPassant,
    "whiteKingSide": whiteKingSide,
    "whiteQueenSide": whiteQueenSide,
    "blackQueenSide": blackQueenSide,
    "blackKingSide": blackKingSide,
    "moveAI": moveAI,
    "gameOver":gameOver }, status = 200)