
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import chess
import chess.engine

from stockfish import Stockfish

from numpy import load
import numpy as np

board = chess.Board()
stockfish = Stockfish(path="static\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
engine = chess.engine.SimpleEngine.popen_uci(r"static\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")


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
    print(move)
    m = isValid(move)
    print(m)
    return JsonResponse({
    "valid": m }, status = 200)
    
def load_board(request):
    return render(request, 'board.html')
    
def home(request):
    return render(request, 'mainpage.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def authenticate(request):
    username = request.POST['Username']
    password = request.POST['Password']
    return render(request, 'mainpage.html',{'Username': username, 'Password': password})
