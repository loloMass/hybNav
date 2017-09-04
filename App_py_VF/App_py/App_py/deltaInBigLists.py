from pylab import *
from matplotlib import *
from math import *

import numpy as np

def deltaInList(list):
    L = [(list[j][i]-list[j][i-1]) for j in range(0,len(list)) for i in range(1, len(list[j]))]
    taille = [len(elt)-1 for elt in list]
    finalList= []
    prev = 0

    for i, index in enumerate(taille):
        finalList.append(L[prev:prev + index])

        prev = prev + index
    return finalList