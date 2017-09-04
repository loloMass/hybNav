from pylab import *
from matplotlib import *
from math import *

import numpy as np

def longilist2kmeter(latlist):
    L = [ 111.11* cos(latlist[j][i]*pi/180) for j in range(len(latlist)) for i in range(0, len(latlist[j]))]
    taille = [len(elt) for elt in latlist]
    longilist2km= []
    prev = 0

    for i, index in enumerate(taille):
        longilist2km.append(L[prev:prev + index])

        prev = prev + index
    return longilist2km

def latlist2kmeter(latlist):
    L = [(111.11* latlist[j][i])for j in range(len(latlist)) for i in range(0, len(latlist[j]))]
    taille = [len(elt) for elt in latlist]
    latliste2km= []
    prev = 0

    for i, index in enumerate(taille):
        latliste2km.append(L[prev:prev + index])

        prev = prev + index
    return latliste2km