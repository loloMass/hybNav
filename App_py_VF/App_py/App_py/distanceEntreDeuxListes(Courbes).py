
from pylab import *
from matplotlib import *
from math import *

import numpy as np

def projection(x, y,a,b):
    L = [(abs((-a[j])*x[j][i] +y[j][i]-b[j]) / sqrt(a[j]**2 +1))for j in range(len(x)) for i in range(0, len(x[j]))]
    taille = [len(elt) for elt in x]
    deviationBetween2graph= []
    prev = 0

    for i, index in enumerate(taille):
        deviationBetween2graph.append(L[prev:prev + index])

        prev = prev + index
    return deviationBetween2graph