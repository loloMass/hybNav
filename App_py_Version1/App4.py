_author_="Massamba"

import numpy as np
import matplotlib.pyplot as plt
from math import *
from pylab import *

"""def delUnusedValues(L, b):
        o = 0;
        l = []
        for i in range(b, len(L)):
            if i<b:
                l=L.remove(L[i])
            l.append(L[b])
            b=b+1

        print (l)
        print (len(l))
        return l
"""

tabAcce=[]

multiple28=[]
indicesPics=[]
pic=[]
picValues=[]

latTransition=[]
latTransitionInOut=[]

def delValue(L,b):
    l = []
    for i, j in enumerate(L):
     if j == b:
      l.append(i)
    return l


#fonction delate convertir la taille de biglist en celle de smallList

def newLength(bigList, smallList,nomListe):

    n = len(bigList) - len(smallList)
    del (bigList[:n])
    lenBigList=len(bigList)
    print(bigList)
    print("le Nouveau nombre d'éléments de la liste du fichier %s" % nomListe,"est:%d  " %lenBigList)
    return (bigList)

                                                        #La fonction pour ouvrir et créer la liste complete

def read(filename):
    with open(filename, 'r') as f:
        for line in f:

            maliste = line.split(';')                   #récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste);                      #taille de la liste de départ

            for i in range(0, taille - 1):              #on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i]);         #on convertit en float

            #print(maliste[0:taille-1]) #afficher la liste
           # print("le nombre d'éléments de la liste du fichier %s" % filename ,"est:%d "  % taille)
            return maliste

                                                        #La fonction pour ouvrir et créer la liste sans les premiers zéros: s'applique aux données GPS
def read_gps(filename):
    with open(filename, 'r') as f:
        for line in f:
            maliste = line.split(';')                   #récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste);                      #taille de la liste de départ
            i=0

            while i < taille - 1:                       #on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i]);         #on convertit en float

                if maliste[i] == 0:                     #si la valeur de la liste =0 on supprime (del)
                   del (maliste[i])
                   i=0;                                 #on revient en avant
                else:                                   #sinon on avance d'un cran
                    i = i + 1;
                taille = len(maliste);                  # nouvelle taille de la liste

            #print(maliste[0:taille-1])                  #afficher la liste
           # print("le nombre d'éléments de la liste du fichier %s" % filename ,"est:%d "  % taille)
            return maliste

                                                        #définition du temps
def tempsList(liste):
    tps=[]
    for x in range (0, len(liste)):
        x=x*0.02                                         #conversion du nombre d'éléments en seconde
        tps.append(x)
    #print(tps)
    return tps


                                                        #Appel des fonction read et read_gps qui lisent les fichiers txt et les concatènent dans une liste

#listes pour les données de l'accéléromètre
xlist=read("xdata.txt");
ylist=read("ydata.txt");
zlist=read("zdata.txt");


#listes pour les données de la boussole
xComplist=read("xCompdata.txt");
yComplist=read("yCompdata.txt");
zComplist=read("zCompdata.txt");


#liste latlist pour la latitude et liste longilist pour la latitude
latlist=read_gps("latdata.txt");
longilist=read_gps("longidata.txt");
longueur=len(longilist);
longueur2=len(latlist);



#liste luxlist pour la lumière
luxlist=read("lightdata.txt");


#Conversion des listes pour les adapter à la taille des listes GPS (latitude et longitude)
luxlist=newLength(luxlist,longilist,'luxlist')
xlist=newLength(xlist,longilist,'xlist')
ylist=newLength(ylist,longilist,'ylist')
zlist=newLength(zlist,longilist,'zlist')
xComplist=newLength(xComplist,longilist,'xComplist')
"""xComplist=newLength(xComplist,longilist,'xComplist')
yComplist=newLength(yComplist,longilist,'yComplist')
zComplist=newLength(zComplist,longilist,'zComplist')"""



def limit(graphdata):

    plt.grid(True)
    xy = graphdata[0].get_xydata()                          #liste de tous les points de la courbes de coordonnées x et y
    o=0;
    l = list(range(len(xy)+1));
    for i,point in enumerate(xy):                           #On parcourt les points de xy d'indice i
        if (point[1]>1000.0 and point[1]<2000.0) or point[1]<2000.0 :             #seuils pour la veleur de la lumière lors de la l'entrée dans le building
            print(i,point)
            l[o]=i
            o=o+1
    #print(l2[0])
            if i ==l[0]:                                   #l[0] est la première valeur qui respecte les seuils
                #plt.plot(point[0], point[1], 'o')
                plt.plot(xy[i][0],xy[i][1],'o')            #dessiner le point de transition
                #plt.show();
                return l[0]



#tracé des courbes avec le point limite

 #tracé de la courbe de la lumière
temps=tempsList(luxlist)
longTps=len(temps)
plt.figure( 'light=f(t)')
graphlux=plt.plot(temps[0:len(luxlist)-1],luxlist[0:len(luxlist)-1],label="light=f(t)"); #tracer la courbe
plt.xlabel('temps (s)')                                            #nom de l'axe x
plt.ylabel('light (lux)')                                          #nom de l'axe y
plt.legend();
pointLimite=limit(graphlux)                                        #point de transition
print("pointLimite",pointLimite)





#tracé de la courbe du GPS
plt.figure('latitude=f(longitude)')
plt.grid(True)                                                      #afficher une grille
graphGps=plt.plot(longilist[0:longueur-1],latlist[0:longueur2-1],label="latitude=f(longitude)"); #tracer la courbe
plt.xlabel('longitude')                                             # nom de l'axe x
plt.ylabel('latitude')                                              # nom de l'axe y
plt.legend();
ptsGps = graphGps[0].get_xydata()                                   #On récupère les points de la courbe du graphe
for k,pt in enumerate (ptsGps ):
    if k==pointLimite:                                              #si l'indice k est égale à l'indice j du point de transition
        plt.plot(ptsGps [k][0],ptsGps [k][1], 'o')                  #mettre le point d'indice k sur la courbe du gps
        #plt.show();                                                 #afficher la courbe

 #tracé des courbes de l'accéléromètre

plt.figure('accelerometer=f(t)')
plt.plot(temps[0:longueur - 1], xlist[0:longueur - 1], label="x=f(t)");
plt.plot(temps[0:longueur - 1], ylist[0:longueur - 1], label="y=f(t)");
plt.plot(temps[0:longueur - 1], zlist[0:longueur - 1], label="z=f(t)");
plt.xlabel('temps (s)')                                              # nom de l'axe x
plt.ylabel('accelerometer')                                          # nom de l'axe y
plt.legend();
#plt.show();


#tracé de la courbe générale de l'accéléromètre en fonction du temps en calculant le module des valeurs


for i in range (0, longueur-1):
    d=xlist[i]*xlist[i]+ylist[i]*ylist[i]+zlist[i]*zlist[i]
    j=sqrt(d)
    tabAcce.append(j)
print ("tabAcce",tabAcce)

#Fonctions somme

def somme(UneListe,taille):
    compteur = 0
    accumulateur = 0
    while compteur < taille:
        accumulateur += UneListe[compteur]
        compteur += 1
    return accumulateur

#Fonction moyenne

def moyenne(UneListe,taille):
    return somme(UneListe,taille) / len(UneListe)

#Intervalles sur lesquels faire la recherche de pics

def intervalles (liste,n,diviseur):
    return [liste[x:x + n] for x, elt in enumerate(liste) if x % diviseur == 0]

#Distinguer les pics

def maxi(t):
    l=[]
    p=[]
    acce_zero=moyenne(t,len(t))
    #print (acce_zero)
    for n in range(1, 12):
        for j, x in enumerate(t[len(t) - 39:len(t) - 10]):
            if t[j] > t[j + n] and t[j] > t[j - n] and t[j]>acce_zero+1:
                #and t[j +3] / (t[j] - 2) < 1

                l.append(j)

        return l               #return [j for j,x in enumerate (t[len(t)-39:len(t)-10]) if t[j]>t[j+n] and t[j]>t[j-n] and t[j-12]/(t[j]-2)<1 and t[j]>acce_zero+2 ]

#Pour dessiner les pics sur le graphe à leur place exacte c'est à dire éviter la répétition

def add (liste, grandeListe):
    l=[]
    for i in range(0,len(grandeListe)):
        for j,elt in enumerate(grandeListe[i]):

           l.append(elt+liste[i])
    return l


def gps2distance(latitudeListe, longitudeListe):

    dist = 6378 * acos(
        sin((latitudeListe[0] * pi) / 180) * sin((latitudeListe[len(latitudeListe) - 2] * pi) / 180) +
        cos((latitudeListe[0] * pi) / 180) * cos((latitudeListe[len(latitudeListe) - 2] * pi) / 180) *
        cos((longitudeListe[len(longitudeListe) - 2] * pi) / 180 - (longitudeListe[0] * pi) / 180))

    return dist*1000


def gpsEnMetre2distanceGrandeListe(latitudeListe, longitudeListe):
    dist=[]
    for j in range(0,len(latitudeListe)-1):
        dist.append( 6378 *1000* acos(
            sin((latitudeListe[j][0] * pi) / 180) * sin((latitudeListe[j][-1] * pi) / 180) +
            cos((latitudeListe[j][0] * pi) / 180) * cos((latitudeListe[j][-1] * pi) / 180) *
            cos(((longitudeListe[j][-1] * pi) / 180) - ((longitudeListe[j][0] * pi)) / 180)))

    return dist


def position2distancePoleNordM(latitudePt, longitudePt,latitudeNordM,longitudeNordM):
    dist = 6378 * acos(
        sin((latitudePt * pi) / 180) * sin((latitudeNordM * pi) / 180) +
        cos((latitudePt * pi) / 180) * cos((latitudeNordM * pi) / 180) *
        cos(((longitudeNordM* pi) / 180 )- ((longitudePt * pi) / 180)))

    return dist*1000

NewListe = intervalles(tabAcce,50,28)                                           #NewListe est la liste des intervalles
temps = tempsList(tabAcce)                                                  #Abscisse du graphe =temps
plt.figure('accelerometer=f(t)')
graphAcce = plt.plot(temps[0:longueur - 1], tabAcce[0:longueur - 1], label="accelerometer=f(t)");


for i in range (1, len(NewListe)):                                          # parcourt la grande liste des intervalles
    indicesPics.append(maxi(NewListe[i]))
    for j in range(0, len(tabAcce) - 1):                                    # parcourt le tableau des valeurs de accelerometre selon z pour trouver les multiples de 28
        if j % 28 == 0 and j is not 0:
            multiple28.append(j)                                            # liste des multiples de 28

for i in range(0,len(indicesPics)):
    for j,elt in enumerate(indicesPics[i]):
           pic.append(elt+multiple28[i])

for elt in pic:
    for i in range (0,len(tabAcce)-1):
        if elt==i:
            picValues.append(tabAcce[elt])
print ("picValues",picValues)


ptsAcce = graphAcce[0].get_xydata()


for k, p in enumerate(ptsAcce):
    if k == pointLimite:                                                    # si l'indice k est égale à l'indice j du point de transition
        plt.plot(ptsAcce[k][0], ptsAcce[k][1], 'o')                         # mettre le point d'indice k sur la courbe du gps
        #print(k)
    # pic = add(multiple28, indicesPics)
    for k1 in range(0, len(pic) - 1):
        # print (pic[k1])
        if picValues[k1] > picValues[k1 + 1] and picValues[k1] > picValues[k1 - 1]:
            i = pic[k1]
            # and pic[k1]+8 <pic[k1+1]
            # si l'indice k est égale à l'indice j du point de transition
            if k == i:
                plt.plot(ptsAcce[k][0], ptsAcce[k][1], 'X')
#plt.show()
print ("indicesPics",indicesPics)
print ("multiple28",multiple28)
print("pic",pic)


#Calcul de la distance parcourure avec des pas de 0.75m

dist=len(pic)*0.75
print ("dist",dist)

#calcul d'une distance orthodromique entre deux points de la terre #6378km est le rayon terrestre

distance =gps2distance(latlist,longilist)                           #distance parcourue calculée avec nos données
print("la distance parcourue dehors est",distance,"m")              #affichage de la distance parcourue


#déterminer la transition le point réel de transition entre l'extérieur et l'intérieur

pointT=[]
def seuil(L):  #fonction pour déterminer les points de luxlist pendant l'entrée au niveau de la porte
    b =[]
    for elt in L:
        for i in range(0,len(elt)-1):
            if (elt[i] - elt[i + 1]) > 0 and elt[i + 1] < 1000:
           # if (elt[i]-elt[i+1]) <=200 and  (elt[i]-elt[i+1])>0 and elt[i+1]<2000 :
                #return elt[i]
                return elt[i+1]



def pointOutIn(liste, taille):
    outIn = 0
    oIindex = 0
    for i in range(0, taille - 1):
        if liste[i] == liste[-2] and liste[i - 1] != liste[-2] and liste[-2] != 0:
            outIn = liste[i - 1]
            oIindex = liste.index(outIn)
    print("outIn", outIn)
    print("oIindex", oIindex)
    return oIindex

def pointInOut(liste, taille):
    inOut = 0
    iOindex=0
    for i in range(0, taille - 1):
        if liste[i] != 0 and liste[i - 1] == 0 and liste[0]==0:
            inOut = liste[i]
            iOindex = liste.index(inOut)
    print("inOut", inOut)
    return iOindex

def axPlusb(x, a,b):
    L = [a[j] * x[j][i] + b[j] for j in range(len(x)) for i in range(0, len(x[j]))]
    taille = [len(elt) for elt in x]
    output = []
    prev = 0

    for i,index in enumerate (taille):
        output.append(L[prev:prev+index])
        prev =prev+index

    return output

def reaLimitOutIn(graphdata,liste):
    plt.grid(True)
    xy = graphdata[0].get_xydata()                          #liste de tous les points de la courbes de coordonnées x et y
    plt.figure("Real transition point")
    graphdata = plt.plot(temps[0:len(liste) - 1], luxlist[0:len(liste) - 1], label="light=f(t)") # tracer la courbe
    plt.xlabel('temps (s)')  # nom de l'axe x
    plt.ylabel('light (lux)')  # nom de l'axe y
    plt.legend();
    o=0;
    l =[]
    nb=[]
    graphListe=[]


    for i,point in enumerate(liste):                           #On parcourt les points de xy d'indice i
            l.append(point)
    oI_index = pointOutIn(latlist, longueur2)
    inter = intervalles(l, 100, 56)
    b=seuil(inter)


    print ("l",liste[oI_index])
    for j,elt in enumerate(liste):
        if elt==b:
            graphListe=liste[liste.index(elt):oI_index]

    print("graphliste",graphListe)

    for j, e in enumerate(xy):
        for i, elt in enumerate(graphListe):
                if e[1] == elt:
                    plt.plot(xy[j][0], xy[j][1], 'X')

    plt.show()
    return b


def longilist2meter(latlist):
    L = [111.11 *1000* cos(latlist[j][i] * pi / 180) for j in range(len(latlist)) for i in range(0, len(latlist[j]))]
    taille = [len(elt) for elt in latlist]
    longilist2m = []
    prev = 0

    for i, index in enumerate(taille):
        longilist2m.append(L[prev:prev + index])

        prev = prev + index
    return longilist2m


def latlist2meter(latlist):
    L = [(111.11 * 1000*latlist[j][i]) for j in range(len(latlist)) for i in range(0, len(latlist[j]))]
    taille = [len(elt) for elt in latlist]
    latliste2m = []
    prev = 0

    for i, index in enumerate(taille):
        latliste2m.append(L[prev:prev + index])

        prev = prev + index
    return latliste2m


def alphaZ(xComplist, lat,lon):
    moyXComplist= []
    newLat=[]
    newLon=[]
    newComp=[]
    deltaXcomp=[]

    coteAdjascent1 = []
    coteOppose1 = []
    alpha1 = []

    direction=[]
    directionAcce = []
    combinedDirection=[]
    for j in range(0, len(lon)):

        coteAdjascent1.append(lon[j][-1] - lon[j][0])
        coteOppose1.append(lat[j][-1] - lat[j][0])
    print ("cote oppose",coteOppose1)
    for j in range(0, len(coteAdjascent1)):
        if coteAdjascent1[j]!=0:
            alpha1.append(arctan((coteOppose1[j] / coteAdjascent1[j]) * pi / 180))

    for i in range (0,len(alpha1)-1):
        if alpha1[i]<0 and alpha1[i+1]<0 and alpha1[i+1]> alpha1[i]:
            direction.append("E")
        elif alpha1[i] < 0  and alpha1[i + 1] < 0 and alpha1[i + 1] < alpha1[i]  :
            direction.append("W")
        elif alpha1[i] > 0 :
            direction.append("D")


    print("t", len(alpha1))


    for j in range(len(xComplist)):
        moyXComplist.append(moyenne(xComplist[j], len(xComplist[j])))
        deltaXcomp.append(xComplist[j][-1] - xComplist[j][0])




    #print(xComplist)
    #print("er", moyXComplist)
    #print(len(moyXComplist))
    #print("deltaxC",deltaXcomp)

    for i, angl in enumerate(moyXComplist):
        #if coteAdjascent1[i] != 0:
            if angl > 0 and angl<= 45 and angl > 315 and angl <= 360:
                directionAcce.append("N")
            elif angl > 45 and angl <= 135:
                directionAcce.append("E")
            elif angl > 135 and angl <= 225:
                directionAcce.append("S")
            elif angl > 225 and angl <= 315:
                directionAcce.append("W")


    #print("d", len(direction))
    #print("op", len(direction))
    #print("dr", directionAcce)
    #print("op1", len(directionAcce))
    plt.figure()
    plt.plot(moyXComplist)
    plt.xlabel('i')  # nom de l'axe x
    plt.ylabel('moyXComplist')  # nom de l'axe y
    #for i, angl in enumerate(moyXComplist):
    print("dA", directionAcce)
    for i in range(0,len(moyXComplist)):
     if coteAdjascent1[i] != 0:

        #first condition from xComplist and second from GPS data
        if alpha1[i-1] < 0 and alpha1[i ] < 0  and alpha1[i]> alpha1[i-1] and moyXComplist[i-1] > 113 and moyXComplist[i-1]<= 158:
            combinedDirection.append("TE")
        elif alpha1[i ]>0 and moyXComplist[i - 1] > 45 and moyXComplist[i - 1] <= 135:
            combinedDirection.append("E")
        elif alpha1[i-1] < 0 and alpha1[i ] < 0  and alpha1[i]<alpha1[i-1] and moyXComplist[i-1] > 203 and moyXComplist[i-1]<= 248  :
            combinedDirection.append("TW")
        elif alpha1[i] > 0 and moyXComplist[i - 1] > 225 and moyXComplist[i - 1] <= 315:
            combinedDirection.append("W")
        elif alpha1[i]>0 and moyXComplist[i-1] > 135 and moyXComplist[i-1]<= 225:
            combinedDirection.append("S")
        else:
            combinedDirection.append("P")

        """if  moyXComplist[i-1] > 45 and moyXComplist[i-1]<= 113 and alpha1[i-1] > 0: #E&D=>E
            combinedDirection.append("E")
            newComp.append(moyXComplist[i-1])
        elif moyXComplist[i-1]> 113 and moyXComplist[i-1]<= 168 and  alpha1[i-1] < 0 and alpha1[i ] < 0  and alpha1[i]> alpha1[i-1]: #E&E=>TE
            combinedDirection.append("TE")
            newComp.append(moyXComplist[i - 1])
        elif moyXComplist[i-1]> 203 and moyXComplist[i-1] <= 248 and alpha1[i-1] < 0 and alpha1[i ] < 0  and alpha1[i ] <alpha1[i-1]:  # W&W=>TW
            combinedDirection.append("TW")
            newComp.append(moyXComplist[i - 1])
        elif moyXComplist[i-1] > 248 and moyXComplist[i-1] <= 315 and alpha1[i-1] > 0: #W&D=>W
            combinedDirection.append("W")
            newComp.append(moyXComplist[i - 1])
        elif moyXComplist[i-1] > 158 and moyXComplist[i-1] <= 203 and alpha1[i-1]>0: #S&D=> S
            combinedDirection.append("S")
            newComp.append(moyXComplist[i - 1])
        elif moyXComplist[i - 1] > 0 and moyXComplist[i - 1] <= 45 and moyXComplist[i - 1] > 315 and moyXComplist[i - 1] <= 360 and alpha1[i - 1] > 0:  # N&D=>N
            combinedDirection.append("N")
            newComp.append(moyXComplist[i - 1])
        elif moyXComplist[i - 1] >158 and moyXComplist[i - 1] <= 203 and alpha1[i-1]<0:
            combinedDirection.append("P")


     else:
         if  moyXComplist[i - 1] > 0 and moyXComplist[i - 1] <= 45 and moyXComplist[i - 1] > 315 and moyXComplist[i - 1] <= 360:
             combinedDirection.append("N")
         #elif moyXComplist[i] > 315 and moyXComplist[i] <= 360:
             #combinedDirection.append("N")
         elif moyXComplist[i] > 45 and moyXComplist[i] <= 135:
             combinedDirection.append("E")
         elif moyXComplist[i] > 112 and moyXComplist[i] <= 158:
             combinedDirection.append("TE")
         elif moyXComplist[i] > 158 and moyXComplist[i]<= 203:
             combinedDirection.append("S")
         elif moyXComplist[i ] > 203 and moyXComplist[i] <= 248:
             combinedDirection.append("TW")
         elif moyXComplist[i] > 248 and moyXComplist[i] <= 315:
             combinedDirection.append("W")"""
         #elif moyXComplist[i] > 198 and moyXComplist[i] <= 302:
             #combinedDirection.append("TW")
         #elif moyXComplist[i] > 108 and moyXComplist[i] <= 162:
             #combinedDirection.append("TE")
    #plt.plot(newComp)
    plt.show()



    print("Cd", combinedDirection)
    print("op", len(combinedDirection))
    #print("lat",newLat)
    #print("lon",newLon)


    return alpha1

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

def ecartType(graphdata,latList,longiList):

    plt.grid(True)
    xy = graphdata[0].get_xydata()                          #liste de tous les points de la courbes de coordonnées x et y
    plt.figure("Real transition point")
    graphdata = plt.plot(longilist[0:longueur - 1], latlist[0:longueur2 - 1]);  # tracer la courbe
    plt.xlabel('longitude')  # nom de l'axe x
    plt.ylabel('latitude')  # nom de l'axe y
    plt.legend();





   #_____________oI_index point de baisse de la lumière au passage de la porte, b premier point lors de la stagnation des valeurs de latitude
    l = []
    for i,point in enumerate(luxlist):                           #On parcourt les points de xy d'indice i
            l.append(point)
    oI_index = pointOutIn(latList, longueur2)
    inter = intervalles(l, 300, 50)
    b = seuil(inter)


  #_______ tracé des droites d'équation latitude= a* longitude + b
    #y=[]
    newLongiValues=[]
    newLatValues=[]
    newLongiValuesEnMetre=[]
    newLatValuesEnMetre=[]
    a=[]
    b=[]
    latIntervalles = intervalles(latList[0:-1], 300, 50) #jusqu'à -1 pour récupérer latlist jusqu'au dernier élément de type float
    longiIntervalles = intervalles(longiList[0:-1], 300, 50)


    for i, elt in enumerate(latIntervalles):
        if (longiIntervalles[i][-1] - longiIntervalles[i][0]) != 0:  #On élimine les cas de division par zéro
            a.append((latIntervalles[i][-1] -latIntervalles[i][0])  / (longiIntervalles[i][-1] - longiIntervalles[i][0]))
            b.append(latIntervalles[i][0] - a[i] * longiIntervalles[i][0])

            newLongiValues.append(longiIntervalles[i]) # La nouvelle liste de valeurs longitudinales de même taille que la liste des coefficients a et b
            newLatValues.append(latIntervalles[i])  # La nouvelle liste de valeurs de latitude de même taille que la liste des coefficients a et b



    y=axPlusb(newLongiValues,a,b) #y= a*x+b avec x la liste des valeurs de  longitude ici newLongiValues

    for i in range(0, len(newLongiValues)):
        plt.plot(newLongiValues[i], y[i]) #Affichage de y en fonction de newLongiValues y= a* newLongiValues + b
        plt.plot(newLongiValues[i], newLatValues[i],'r', linewidth=2.5)
        plt.plot(longiIntervalles[i], latIntervalles[i], 'r', linewidth=2.5)

    plt.xlabel('longitude')  # nom de l'axe x
    plt.ylabel('latitude')  # nom de l'axe y
    plt.legend();
    plt.show()

    #_______calcul d'écart type


    moyInterLongi=[]
    ecartTypeLat=[]
    ecartTypeLongi = []

    for i, elt1 in enumerate(y):
        j = 0
        acc = 0
        while j < len(latIntervalles[i]):

            acc += (latIntervalles[i][j] - y[i][j]) ** 2
            j += 1
            # print ("acc",acc)
        variance = acc / len(latIntervalles[i])
        ecartTypeValues = sqrt(variance)
        ecartTypeLat.append(ecartTypeValues)


    # _______calcul d'écart  entre chaque point de la courbe d'origine et les différentes droites

    ecart=projection(newLongiValues,newLatValues,a,b)
    print("écart",ecart)

    # _______Détection d'un tournant et d'une marche en ligne droite
    """ moyEcart = []
    sumEcart=[]
    for i in range(0,len(ecart)):
        moyEcart.append(moyenne(ecart[i], len(ecart[i])))
    print("moyEcart", moyEcart)
    print("indexMinMoyEcart", moyEcart.index(min(moyEcart)))
    print("minMoyEcart",min(moyEcart))
    print("indexMaxMoyEcart", moyEcart.index(max(moyEcart)))
    print("maxMoyEcart",max(moyEcart))

    for i in range(0,len(ecart)):
        sumEcart.append(somme(ecart[i], len(ecart[i])))
    print("sumEcart", sumEcart)
    print("indexMinsumEcart", sumEcart.index(min(sumEcart)))
    print("minsumEcart",min(sumEcart))
    print("indexMaxsumEcart", sumEcart.index(max(sumEcart)))
    print("maxsumEcart",max(sumEcart))"""

    """ print ("r",sumEcart[40:52])
    print("r", sumEcart[79:110])
    print("r", sumEcart[80:88])"""
    # _______Distinction d'une zone de perturbation et d'un tournant



    return y


m=reaLimitOutIn(graphlux, luxlist)
#print("m",m)

n=ecartType(graphGps, latlist,longilist)
#print("n",n)


iO_index=pointInOut(latlist,longueur2)
oI_index=pointOutIn(latlist,longueur2)



 #tracé des courbes de la boussole


DeviationIllkirch=[]
xComplistCalibree=[]
tempsC=tempsList(xComplist)
"""for i in range (0,len(xComplist)-1):
    DeviationIllkirch.append(2.066667)
    xComplistReal.append(xComplist[i]-DeviationIllkirch[i])"""

def calibrageBoussole(liste):
    listeCalibree=[]
    for i in range(0, len(liste)-1):
        if liste[i] < 0:
            listeCalibree.append(liste[i] + 360)
        elif liste[i] > 0:
            listeCalibree.append(liste[i])
        elif liste[i] == 0:
            listeCalibree.append(liste[i])
    return listeCalibree


xComplistCalibree=calibrageBoussole(xComplist)


latIntervalles = intervalles(latlist[0:-1], 300,50)  # jusqu'à -1 pour récupérer latlist jusqu'au dernier élément de type float
longiIntervalles = intervalles(longilist[0:-1], 300, 50)
xCompIntervalles=intervalles(xComplistCalibree[0:-1], 300, 50)
latliste2m = latlist2meter(latIntervalles)
longilist2m = longilist2meter(latIntervalles)


print("azi", alphaZ(xCompIntervalles,latIntervalles,longiIntervalles))
print("xComplistCalibrée",xComplistCalibree)


plt.figure('compass=f(t)')
plt.plot(tempsC[0:len(xComplist)-1],xComplist[0:len(xComplist)-1],label="xComp=f(t)");
plt.plot(tempsC[0:len(xComplist)-1],yComplist[0:len(xComplist)-1],label="yComp=f(t)");
plt.plot(tempsC[0:len(xComplist)-1],xComplistCalibree[0:len(xComplist)],label="xCompCalibree=f(t)");
plt.plot(tempsC[0:len(xComplist)-1],zComplist[0:len(xComplist)-1],label="zComp=f(t)");
plt.xlabel('temps (s)')                                                     #nom de l'axe x
plt.ylabel('Boussole (degrées)')                                                      #nom de l'axe y
plt.legend() ;
plt.show();


print ("h",position2distancePoleNordM(48.52,7.74,84.826,-129.946))
print("g",gpsEnMetre2distanceGrandeListe(latIntervalles,longiIntervalles))
#lok=arctan(((48.3/cos(-0.004))/position2distancePoleNordM(48.3,7.1,84.826,-129.946))*pi/180)
#print (lok)

#Mettre les indices du tableau de pics sur une échelle de temps
"""def timeBetween2pic(listePic):
    tibtw2Pic = []
    for j in range(0, len(listePic )- 1):
        tibtw2Pic.append((listePic[j + 1] - listePic[j]) * 0.02)
    #print(tibtw2Pic)
    temps2parcourt=sum(tibtw2Pic)
    print("le temps de parcourt est ", temps2parcourt, "s")
    return tibtw2Pic

tpsbtw2Pic=timeBetween2pic(pic)"""


"""
inOut=0
latTransition=[]
latTransitionInOut=[]
for i in range(0,longueur2-1):
    if latlist[i]==latlist[-2] and latlist[-2]!=0 :
        latTransition.append(i)

for i in range(0,longueur2-1):
    if latlist[i]!=0:
        latTransitionInOut.append(latlist[i])
        inOut=latTransitionInOut[0]
print (len(latTransition))
print(latlist[-2])
print (inOut)"""

