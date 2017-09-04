from pylab import *
from matplotlib import *
from math import *

import numpy as np


def absBetweendeuxListes(yCourbe, yCalculé):
    L = [abs(yCourbe[j][i] - yCalculé[j][i] )for j in range(len(yCourbe)) for i in range(0, len(yCourbe[j]))]
    taille = [len(elt) for elt in yCourbe]
    output = []
    prev = 0

    for i, index in enumerate(taille):
        output.append(L[prev:prev + index])

        prev = prev + index
    return output