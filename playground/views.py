from email import message
from turtle import rt
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

board.has_legal_en_passant()
bool(chess.BB_H1)
bool(chess.BB_A1)
bool(chess.BB_A8)
bool(chess.BB_H8)
board.is_checkmate()
# Create your views here.
def isValid(move):
    try:
        board.push_san(move)
        return True
    except ValueError:
        return False


def boardStates(request):
    request.GET.get(message)
    legalEnPassant =  board.has_legal_en_passant()
    whiteKingSide = bool(chess.BB_H1)
    whiteQueenSide = bool(chess.BB_A1)
    blackQueenSide = bool(chess.BB_A8)
    blackKingSide = bool(chess.BB_H8)
    print(legalEnPassant)
    print(whiteKingSide)
    print(whiteQueenSide)
    print(blackQueenSide)
    print(blackKingSide)
    return JsonResponse({"legalEnPassant": legalEnPassant,
    "whiteKingSide": whiteKingSide,
    "whiteQueenSide": whiteQueenSide,
    "blackQueenSide": blackQueenSide,
    "blackKingSide": blackKingSide,
     },status = 200)

def validMove(request):
    move = request.POST.get('moveMade')
    return JsonResponse({
    "valid": isValid(move)}, status = 200)
    
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
