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

import waste2

User = waste2.Username
print(User)







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



