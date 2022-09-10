
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import chess
import chess.engine



from numpy import load
import numpy as np


board = chess.Board()


# Create your views here.
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


