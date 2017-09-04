from pylab import *
from matplotlib import *
from math import *

import numpy as np

def somme(UneListe,taille):
    compteur = 0
    accumulateur = 0
    while compteur < taille:
        accumulateur += UneListe[compteur]
        compteur += 1
    return accumulateur

def moyenne(UneListe,taille):
    return somme(UneListe,taille) / len(UneListe)


def tempsList(liste):
    tps=[]
    for x in range (0, len(liste)):
        x=x*0.02                                         #conversion du nombre d'éléments en seconde
        tps.append(x)
    #print(tps)
    return tps

def maxi(t):
    l=[]
    p=[]
    acce_zero=moyenne(t,len(t))
    for n in range(1, 11):
        for j, x in enumerate(t[len(t) - 39:len(t) - 11]):
              if t[j] > t[j +n] and t[j] > t[j - n] and t[j - 11]/(t[j]-2)<0.90 and t[j + 11]/(t[j]-2)<0.90 and t[j] >= acce_zero :
                       l.append(j)

        return l






def detectionPic(listeOriginale,k,diviseur):
    L=[listeOriginale[x:x + k] for x, elt in enumerate(listeOriginale) if x % diviseur == 0]
    T = [maxi(L[i]) for i in range(0,len(L)) ]
    picsValues=[]
    realIndicePics=[]
    finalIndicesPics=[]
    tps = tempsList(listeOriginale)
    longueur = len(listeOriginale)
    plt.figure()
    grapheAcce = plt.plot(tps[0:longueur - 1], listeOriginale[0:longueur - 1], label="accelerometer=f(t)")
    indicesAcce = grapheAcce[0].get_xydata()
    multipl28 = [y for y, elt in enumerate(listeOriginale) if y % diviseur==0]
    NL=[]
    for i in range(0, len(T)):
        for j, elt in enumerate(T[i]):
             realIndicePics.append(elt + multipl28[i])

    for k1 in range(0,len(realIndicePics)-1):
        picsValues.append(listeOriginale[realIndicePics[k1]])

        if realIndicePics[k1+1]-realIndicePics[k1]>5 and listeOriginale[realIndicePics[k1]]>listeOriginale[realIndicePics[k1+1]]:
            finalIndicesPics.append(realIndicePics[k1])
        elif realIndicePics[k1+1]-realIndicePics[k1]>5 and listeOriginale[realIndicePics[k1]]<listeOriginale[realIndicePics[k1+1]]:
            finalIndicesPics.append(realIndicePics[k1+1])
        elif realIndicePics[k1 + 1] - realIndicePics[k1] <5 and listeOriginale[realIndicePics[k1]] > listeOriginale[realIndicePics[k1 + 1]]:
            finalIndicesPics.append(realIndicePics[k1])
        elif realIndicePics[k1 + 1] - realIndicePics[k1] > 5 and listeOriginale[realIndicePics[k1]] < listeOriginale[realIndicePics[k1 + 1]]:
            finalIndicesPics.append(realIndicePics[k1 + 1])

    for j in range(0, len(finalIndicesPics)-1):
        if finalIndicesPics[j]!=finalIndicesPics[j+1] and finalIndicesPics[j+1]-finalIndicesPics[j]>15:
            NL.append(finalIndicesPics[j])

    # Tracé des pics
    for k, p in enumerate(listeOriginale):
         for k1 , pt in enumerate(NL):
                if  k==pt:
                  plt.plot(indicesAcce[k][0], indicesAcce[k][1], 'X')
    plt.legend()
    plt.show()

    return NL