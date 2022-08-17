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

def boardStates(request):
    message = "Sent back Python response"
    return JsonResponse({"response": message,
    "fish": "hiii",
    "tryMe": "tryme"}, status = 200)

def validMove(request):
    text = request.POST.get('message')
    message = "Sent back Python response"
    return JsonResponse({"response": message,
    "fish": "hiii",
    "tryMe": "tryme"}, status = 200)
    
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
