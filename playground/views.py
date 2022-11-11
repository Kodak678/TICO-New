
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import chess
import chess.engine
import random
import numpy


board = chess.Board()


# Create your views here.


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
        # Scorset = []
        # Scorset.append(getScore(board,not(board.turn)))
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
    "blackKingSide": blackKingSide,
     },status = 200)

def validMove(request):
    move = str(request.POST.get('move'))
    m = isValid(move)
    return JsonResponse({
    "valid": m }, status = 200)
    
def load_board(request):
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


    child_nodes = list(board.legal_moves)
    move = random.choice(child_nodes)
    board.push(move)
    moveAI = str(move)


    # Stockfish = chess.engine.SimpleEngine.popen_uci("templates\stockfish.exe")
    # moveAI = Stockfish.play(board,chess.engine.Limit(time=0.1))
    # Stockfish.quit()
    # board.push(moveAI.move)
    # moveAI = str(moveAI.move)  

    
    return JsonResponse({"legalEnPassant": legalEnPassant,
    "whiteKingSide": whiteKingSide,
    "whiteQueenSide": whiteQueenSide,
    "blackQueenSide": blackQueenSide,
    "blackKingSide": blackKingSide,
    "moveAI": moveAI }, status = 200)