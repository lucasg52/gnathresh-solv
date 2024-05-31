import numpy
import math

myarray = numpy.array(
        [i ** math.pi for i in range(1,1000)]
        )

numpy.save("outfile.npy",myarray, allow_pickle = False)
