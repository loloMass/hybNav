from pylab import *
from matplotlib import *
from math import *

import numpy as np


def read(filename):
    with open(filename, 'r') as f:
        for line in f:

            maliste = line.split(';')                   #récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste)                      #taille de la liste de départ

            for i in range(0, taille - 1):              #on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i])         #on convertit en float

            #print(maliste[0:taille-1]) #afficher la liste
           # print("le nombre d'éléments de la liste du fichier %s" % filename ,"est:%d "  % taille)
            return maliste


#listes pour les données de l'accéléromètre
xlist=read("xdata.txt")
ylist=read("ydata.txt")
zlist=read("zdata.txt")

tabAcce=[]
for i in range (0, len(xlist)-1):
    d=xlist[i]*xlist[i]+ylist[i]*ylist[i]+zlist[i]*zlist[i]
    j=sqrt(d)
    tabAcce.append(j)


x = [[1, 2, 3, 5], [1, 2, 4],[1, 2, 4],[1, 2, 3, 5],[9,8]]
y = [[6,9,0,7], [1, 2, 4],[9,7,8],[1, 2, 3, 5],[9,8]]
a = [1, 2,5,9,8]
b = [9, 4,4,3,0]
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
def absBetweendeuxListes(yCourbe, yCalculé):
    L = [abs(yCourbe[j][i] - yCalculé[j][i] )for j in range(len(yCourbe)) for i in range(0, len(yCourbe[j]))]
    taille = [len(elt) for elt in yCourbe]
    output = []
    prev = 0

    for i, index in enumerate(taille):
        output.append(L[prev:prev + index])

        prev = prev + index
    return output

def projection(x, y,a,b):
    L = [(abs((-a[j])*x[j][i] +y[j][i]-b[j]) / sqrt(a[j]**2 +1))for j in range(len(x)) for i in range(0, len(x[j]))]
    taille = [len(elt) for elt in x]
    deviationBetween2graph= []
    prev = 0

    for i, index in enumerate(taille):
        deviationBetween2graph.append(L[prev:prev + index])

        prev = prev + index
    return deviationBetween2graph

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

def gps2distance(latitudeListe, longitudeListe):
    dist = 6378 * acos(
        sin((latitudeListe[0] * pi) / 180) * sin((latitudeListe[len(latitudeListe) - 2] * pi) / 180) +
        cos((latitudeListe[0] * pi) / 180) * cos((latitudeListe[len(latitudeListe) - 2] * pi) / 180) *
        cos((longitudeListe[len(longitudeListe) - 2] * pi) / 180 - (longitudeListe[0] * pi) / 180))

    return dist*1000

def azimuth(latitudeEnkm, longitudeEnkm):
    coteAdjascent=[]
    coteOppose=[]
    alpha=[]
    for j in range(0,len(longitudeEnkm)):
        coteAdjascent.append(longitudeEnkm[j][-1]-longitudeEnkm[j][0])
        coteOppose.append(latitudeEnkm[j][-1]-latitudeEnkm[j][0])
    print(coteAdjascent)
    print(coteOppose)
    for j in range(0,len(coteAdjascent)):
        alpha.append(arctan((coteOppose[j]/coteAdjascent[j])*pi/180))
    print(alpha)

def somme(UneListe,taille):
    compteur = 0
    accumulateur = 0
    while compteur < taille:
        accumulateur += UneListe[compteur]
        compteur += 1
    return accumulateur

def moyBoussole(xComplist):
    accumulateur = 0
    compteur=0
    L=[]
    for j in range(len(xComplist)):
        while compteur < len(xComplist[j]):
                accumulateur += xComplist[j][compteur]
                compteur+= 1

        L.append(accumulateur/len(xComplist[j]))

    return L


"""print (projection(x,y,a,b))
Y=axPlusb(x,a,b)
print (Y)
print(x)
for i in range(0,len(x)):
    plt.plot(x[i],Y[i])
plt.plot(x[0], y[0],'r',linewidth=3)
plt.plot(x[0], Y[0],'g',linewidth=3)
plt.show()

t=[[8,9,0,7],[7,6,5,0]]
t1=[[7,6,5,0], [7,6,5,0]]
print(absBetweendeuxListes(t,t1))

latList=[[48.9,47.8],[46.4,47.8]]
#longilist=[[7.6, 7.9],[7.8, 7.5]]
print("0",latList)
print ("1",latlist2kmeter(latList))
print ("2",longilist2kmeter(latList))
azimuth(latlist2kmeter(latList),longilist2kmeter(latList))

tes=[[1,2],[6,4]]"""

def deltaInList(list):
    L = [(list[j][i]-list[j][i-1]) for j in range(0,len(list)) for i in range(1, len(list[j]))]
    taille = [len(elt)-1 for elt in list]
    finalList= []
    prev = 0

    for i, index in enumerate(taille):
        finalList.append(L[prev:prev + index])

        prev = prev + index
    return finalList

#print("r",deltaInList(tes))

#picComp=[45,90,180,270,360]

def compDist(picComp):

    xDist=[]
    yDist=[]
    Ax=[]
    Ay=[]

    long_pas=0.60 #m
    #Ax[1]=long_pas * sin(picComp[0] * 180 / pi) + Ax[0]

    for i in range(0,len(picComp)-1):
        Ax.append(0)
        Ay.append(0)
    for i in range(1, len(picComp)-1):
        Ax[i]=long_pas * sin(picComp[i-1]*pi/180) + Ax[i-1]
        Ay[i]= long_pas * cos(picComp[i-1] *pi/180) + Ay[i-1]
    for i in range(0, len(picComp) -1):
        xDist.append(Ax[i])
        yDist.append(Ay[i])

    print(xDist,"len",len(xDist))
    plt.figure()
    plt.plot(xDist,yDist)
    plt.show()

#compDist(picComp)

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

print(detectionPic(tabAcce,50,28))

print(moyenne([1,0,0,0],len([1,0,0,2])))