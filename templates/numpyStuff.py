from array import array
import numpy

AIboard = numpy.zeros((1, 8, 8), dtype=numpy.int8)
fake = numpy.ones((1,8,8), dtype=numpy.int8).tolist()
b = numpy.load("trying.npy")

BoardSnaps = []

for i in range(0,4):
    BoardSnaps.append(fake)

for snap in BoardSnaps:
    b = numpy.concatenate((b,snap))
numpy.save("trying.npy",b)
print(numpy.load("trying.npy"))