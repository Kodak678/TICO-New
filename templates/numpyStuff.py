from array import array
import numpy




def CreateSaveFiles():
    AIboard = numpy.zeros((1, 8, 8), dtype=numpy.int8)
    Scores = [0]
    Scores = numpy.array(Scores)
    numpy.save("Boards.npy",AIboard)
    numpy.save("Scores.npy",Scores)

# fake = numpy.ones((1,8,8), dtype=numpy.int8).tolist()
# b = numpy.load("trying.npy")

# BoardSnaps = []

# for i in range(0,4):
#     BoardSnaps.append(fake)

# for snap in BoardSnaps:
#     b = numpy.concatenate((b,snap))
# numpy.save("trying.npy",b)
# print(numpy.load("trying.npy"))
AIboard = numpy.ones((1, 8, 8), dtype=numpy.int8)
Scores = [32]


def SaveBoard(Boardsnaps,Boardscores):
    
    Boards = numpy.load("Boards.npy")
    for snap in Boardsnaps:
        Boards = numpy.concatenate((Boards,snap))
    numpy.save("Boards.npy",Boards)

    Scores = numpy.load("Scores.npy")
    Scores = numpy.concatenate((Scores,Score))
    numpy.save("Scores.npy",Scores)

CreateSaveFiles()
# SaveBoard(AIboard,Scores)
print(numpy.load("Boards.npy"))
print(numpy.load("Scores.npy"))