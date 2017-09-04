from pylab import *
from matplotlib import *
from math import *

import numpy as np

def axPlusb(x, a,b):
    L = [a[j] * x[j][i] + b[j] for j in range(len(x)) for i in range(0, len(x[j]))]
    print(L)
    taille = [len(elt) for elt in x]
    print(taille)
    output = []
    prev = 0

    for i,index in enumerate (taille):

        output.append(L[prev:prev+index])

        prev =prev+index


    return output