import chess
import chess.engine

from stockfish import Stockfish

from numpy import load
import numpy as np

stockfish = Stockfish(path="./stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")
engine = chess.engine.SimpleEngine.popen_uci(r"./stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")


































