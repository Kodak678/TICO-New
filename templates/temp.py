import random
import chess
import chess.engine
import numpy 
import tensorflow as tf
from keras import models
import os
import sqlite3
Boardsnaps = []
Boardscores = []
board = chess.Board()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Tells program to ignore an unimportant warning

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






def SaveBoardData(board): #Creates and stores a picture of the chess board in this instant and records the score as well.
        AIboard = ConvertToAIboard(board)
        Score = getScore(board,not(board.turn))
        Boardsnaps.append(AIboard)
        Boardscores.append(Score)
        SaveBoard(Boardsnaps,Boardscores)


def SaveBoard(Boardsnaps,Boardscores):
    numpy.save("ManyBoards.npy",Boardsnaps, True)
    numpy.save("ManyScores.npy",Boardscores, True)








def generate_data(): #To generate data for my heuristic model to learn from.
    temp_board = chess.Board()

    while not(temp_board.is_game_over()):
        child_nodes = list(temp_board.legal_moves)
        move = random.choice(child_nodes)
        temp_board.push(move)
        SaveBoardData(temp_board)


# for i in range(0,10):  #All player's weights should be initialized with some exposure to some data    
#     generate_data()  # to create the data needed

# This ^ generates about 1750 board snaps and corresponding board scores which are stored in ManyBoards.npy and ManyScores.npy


#black win
# SaveBoardData(board)
# board.push_san("f2f4")
# SaveBoardData(board)
# board.push_san("e7e5")
# SaveBoardData(board)
# board.push_san("g2g4")
# SaveBoardData(board)
# board.push_san("d8h4")
# SaveBoardData(board)


#white win
# SaveBoardData(board)
# board.push_san("e2e4")
# SaveBoardData(board)
# board.push_san("g7g5")
# SaveBoardData(board)
# board.push_san("f1c4")
# SaveBoardData(board)
# board.push_san("f7f5")
# SaveBoardData(board)
# board.push_san("d1h5")
# SaveBoardData(board)



x_test = numpy.load("TestBoards.npy")
y_test = numpy.load("TestScores.npy")
y_test = numpy.asarray(y_test / abs(y_test).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)


def create_model():
    model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape = (14,8,8)), 
                                        tf.keras.layers.Dense(128, activation=tf.keras.activations.relu), 
                                        tf.keras.layers.Dense(32, activation=tf.keras.activations.relu),    
                                        tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid),
                                        ])
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss = tf.keras.losses.mean_squared_error, metrics=["accuracy"])
    return model

def train_model(user):
    x = numpy.load("Boards.npy")
    y = numpy.load("Scores.npy")
    y = numpy.asarray(y / abs(y).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)
    model = models.load_model(f'./models/{user}')
    model.fit(x,y,epochs=100)
    model.save(f'./models/{user}')


# x = numpy.load("ManyBoards.npy")
# y = numpy.load("ManyScores.npy")
# y = numpy.asarray(y / abs(y).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)
# model = create_model()
# user = "TICO"
# model = models.load_model(f'./models/{user}')
# model.fit(x,y,epochs=100)
# model = create_model()
# model.load_weights(f'./users/TICOweights/TICO')
# model.save_weights(f'./users/TICOweights/{user}')
# board.push_san("f2f4")

# x = ConvertToAIboard(board)
# print(x)
# x = x.reshape(1,14,8,8)
# print(model.predict(x))


# print(x)

# 0.0026753023266792297

# 0.011421936564147472

# results = model.evaluate(x_test, y_test, batch_size=128)
# print("test loss, test acc:", results)

# results = model.evaluate(x_test, y_test, batch_size=128)
# relative = (( 0.0006020597647875547 - results ) / 0.0006020597647875547) *100

# print(relative)

# Username = "TICO"
# def evaluate_model():
#     results = model.evaluate(x_test, y_test, batch_size=128)
#     relative = (( 0.0006020597647875547 - results ) / 0.0006020597647875547) *100    



# conn = sqlite3.connect('users.db')
# c = conn.cursor()

# c.execute("""CREATE TABLE UserInfo (    
#     Username text,
#     Password text,
#     FirstName text,
#     LastName text,
#     Email text,
#     relative float
# )""")
# Username,Password, FirsName, LastName, Email, Relative = "TICOOO", "1dsdsds4sdsdsdsdsd", "GAME", "BUTTLER", "BOACH@", 0.0

# c.execute("INSERT INTO UserInfo VALUES (?,?,?,?,?,?)", (Username,Password, FirsName, LastName, Email, Relative))
# records = c.execute("SELECT * FROM UserInfo")
# for record in records:
#     print(record)
# conn.commit()
# conn.close()


class User:
    def __init__(self,Username, Password,Firstname, Lastname, Email, relative):
        self.Username = Username
        self.Password = Password
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Email = Email
        self.relative = relative
     

    def getUsername(self):
        return self.Username

    def getFirstname(self):
        return self.Firstname

    def getLastname(self):
        return self.Lastname

    def getEmail(self):
        return self.Email

    def getrelative(self):
        return self.relative

    def resetPassword(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        words = ["Chess", "Board", "Pawn", "Knights", "king"]
        code = random.choice(words)
        count = 0
        for i in code:
            count+= ord(i)
        tempPass = self.Password - count
        with conn:
            c.execute("UPDATE UserInfo SET Password = (:tempPass)  WHERE Username = (:Username)", {'Username': self.Username, 'tempPass': tempPass})

    def updateRelative(self, newRelative):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE UserInfo SET relative = (:Relative) WHERE Username = (:Username)""", 
            {'Username': self.Username, 'Relative':newRelative})

    def updateDetails(self,Password,Firstname, Lastname, Email):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE UserInfo SET Password = (:Password), 
            Firstname = (:Firstname), Lastname = (:Lastname), 
            Email = (:Email)  WHERE Username = (:Username)""", 
            {'Username': self.Username, 'Password': Password, 'Firstname': Firstname, 'Lastname': Lastname, 'Email': Email})


    


# User1 = User('TICOOO', '1dsdsds4sdsdsdsdsd', 'GAME', 'BUTTLER', 'BOACH@', 0.0)
# User1.updateDetails('1dsdsds4', 'GAME', 'BUTTLER', 'BOACH@')



# LoggedInUser = ""
# conn = sqlite3.connect('users.db')
# c = conn.cursor()
# record = c.execute("SELECT * FROM UserInfo")
# for r in record:
#     print(r)
# conn.commit()
# conn.close()


# c.execute("SELECT * FROM UserInfo WHERE Username = (:Username) AND Password = (:Password)", {'Username': 'TICOOO', 'Password': '1dsdsds4'})

# if len(c.fetchall()) == 1:
#     with conn:
#         record = c.execute("SELECT Username, Password, Firstname,Lastname, Email, relative FROM UserInfo WHERE Username = 'TICOOO' ")
#         r = list(record)
#     User1 = User(r[0][0],r[0][1],r[0][2],r[0][3],r[0][4],r[0][5])
#     LoggedInUser = User1
# User1.updateRelative(5.9)
























# conn = sqlite3.connect('users.db')
# c = conn.cursor()
# records = c.execute("SELECT * FROM UserInfo") 
# for record in records:
#     print(record)
# conn.commit()
# conn.close()
# x_test = numpy.load("TestBoards.npy")
# y_test = numpy.load("TestScores.npy")
# y_test = numpy.asarray(y_test / abs(y_test).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)

# x = numpy.load("ManyBoards.npy")
# y = numpy.load("ManyScores.npy")
# y = numpy.asarray(y / abs(y).max() / 2 + 0.5, dtype=numpy.float32) # normalization (0 - 1)

# user = "bat"
# model = models.load_model(f'./models/{user}')
# model.fit(x,y,epochs=100)
# model.save(f'./models/{user}')
# results = model.evaluate(x_test, y_test, batch_size=128)
# print("test loss, test acc:", results)


# 0.0006020597647875547
# 0.0059497058391571045





