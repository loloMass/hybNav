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
            taille = len(maliste)                      #taille de la liste de départ

            for i in range(0, taille - 1):              #on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i])         #on convertit en float

            #print(maliste[0:taille-1]) #afficher la liste
           # print("le nombre d'éléments de la liste du fichier %s" % filename ,"est:%d "  % taille)
            return maliste

                                                        #La fonction pour ouvrir et créer la liste sans les premiers zéros: s'applique aux données GPS
def read_gps(filename):
    with open(filename, 'r') as f:
        for line in f:
            maliste = line.split(';')                   #récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste)                      #taille de la liste de départ
            i=0

            while i < taille - 1:                       #on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i])        #on convertit en float

                if maliste[i] == 0:                     #si la valeur de la liste =0 on supprime (del)
                   del (maliste[i])
                   i=0                                 #on revient en avant
                else:                                   #sinon on avance d'un cran
                    i = i + 1
                taille = len(maliste)                  # nouvelle taille de la liste

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
xlist=read("xdata.txt")
ylist=read("ydata.txt")
zlist=read("zdata.txt")


#listes pour les données de la boussole
xComplist=read("xCompdata.txt")
yComplist=read("yCompdata.txt")
zComplist=read("zCompdata.txt")


#liste latlist pour la latitude et liste longilist pour la latitude
latlist=read_gps("latdata.txt")
longilist=read_gps("longidata.txt")
longueur=len(longilist)
longueur2=len(latlist)



#liste luxlist pour la lumière
luxlist=read("lightdata.txt")


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
    o=0
    l = list(range(len(xy)+1))
    for i,point in enumerate(xy):                           #On parcourt les points de xy d'indice i
        if (point[1]>5000.0 and point[1]<15000.0) :             #seuils pour la veleur de la lumière lors de la l'entrée dans le building
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
#plt.figure( 'light=f(t)')
graphlux=plt.plot(temps[0:len(luxlist)-1],luxlist[0:len(luxlist)-1],label="light=f(t)") #tracer la courbe
plt.xlabel('temps (s)')                                            #nom de l'axe x
plt.ylabel('light (lux)')                                          #nom de l'axe y
plt.legend()
pointLimite=limit(graphlux)                                        #point de transition
print("pointLimite",pointLimite)





#tracé de la courbe du GPS
#plt.figure('latitude=f(longitude)')
plt.grid(True)                                                      #afficher une grille
graphGps=plt.plot(longilist[0:longueur-1],latlist[0:longueur2-1],label="latitude=f(longitude)") #tracer la courbe
plt.xlabel('longitude')                                             # nom de l'axe x
plt.ylabel('latitude')                                              # nom de l'axe y
plt.legend()
ptsGps = graphGps[0].get_xydata()                                   #On récupère les points de la courbe du graphe
for k,pt in enumerate (ptsGps ):
    if k==pointLimite:                                              #si l'indice k est égale à l'indice j du point de transition
        plt.plot(ptsGps [k][0],ptsGps [k][1], 'o')                  #mettre le point d'indice k sur la courbe du gps
        #plt.show();                                                 #afficher la courbe

 #tracé des courbes de l'accéléromètre

#plt.figure('accelerometer=f(t)')
plt.plot(temps[0:longueur - 1], xlist[0:longueur - 1], label="x=f(t)")
plt.plot(temps[0:longueur - 1], ylist[0:longueur - 1], label="y=f(t)")
plt.plot(temps[0:longueur - 1], zlist[0:longueur - 1], label="z=f(t)")
plt.xlabel('temps (s)')                                              # nom de l'axe x
plt.ylabel('accelerometer')                                          # nom de l'axe y
plt.legend()
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
    for n in range(1, 11):
        for j, x in enumerate(t[len(t) - 39:len(t) - 11]):
              if t[j] > t[j +n] and t[j] > t[j - n] and t[j] > acce_zero+2.5 :
                       l.append(j)

        return l
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
def gpsDist(latitudeListe, longitudeListe,dep,arr):

    dist = 6378 *1000* acos(
        sin((latitudeListe[dep] * pi) / 180) * sin((latitudeListe[arr] * pi) / 180) +
        cos((latitudeListe[dep] * pi) / 180) * cos((latitudeListe[arr] * pi) / 180) *
        cos((longitudeListe[arr] * pi) / 180 - (longitudeListe[dep] * pi) / 180))
    return dist

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

#___________________________________________________________________________Gestion des pics



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

def relationPicComp(indPics,valComp):
    relPicComp=[]
    for i, elt in enumerate(indPics):
         relPicComp.append(valComp[elt])
    return relPicComp

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
        Ay[i]= long_pas * cos(picComp[i-1]*pi/180) + Ay[i-1]
    for i in range(0, len(picComp) - 1):
        xDist.append(Ax[i])
        yDist.append(Ay[i])

    print(xDist,"len",len(xDist))
    plt.figure()
    plt.plot(xDist,yDist)
    plt.show()




#Calcul de la distance parcourue avec des pas de 0.72m

dist=(len(pic[587:-1])/2)*0.75




#___________________________________________________________________________Fin de gestion des pics


#calcul d'une distance orthodromique entre deux points de la terre #6378km est le rayon terrestre

distance =gps2distance(latlist,longilist)                           #distance parcourue calculée avec nos données


#déterminer la transition le point réel de transition entre l'extérieur et l'intérieur

pointT=[]
def seuil(L):  #fonction pour déterminer les points de luxlist pendant l'entrée au niveau de la porte
    b =[]
    for elt in L:
        for i in range(0,len(elt)-1):
            if (elt[i] - elt[i + 1]) > 0 and elt[i + 1] < 1000:
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
    #plt.grid(True)
    xy = graphdata[0].get_xydata()                          #liste de tous les points de la courbes de coordonnées x et y
    #plt.figure("Real transition point")
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
    inter = intervalles(l, 300, 50)
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

def deltaInList(list):
    L = [(list[j][i]-list[j][i-1]) for j in range(0,len(list)) for i in range(1, len(list[j]))]
    taille = [len(elt)-1 for elt in list]
    finalList= []
    prev = 0

    for i, index in enumerate(taille):
        finalList.append(L[prev:prev + index])

        prev = prev + index
    return finalList

def capAcceComp(valComp):
    dist60 = []
    plt.figure()
    for x in range(0, len(valComp)):
        x = x * 60 # conversion du nombre d'éléments en seconde
        dist60.append(x)

    plt.plot(dist60,valComp)
    plt.show()

def moyDeltaInGps(biglon,biglat):
    moyDeltaInLat = []
    moyDeltaInLon = []
    deltaInlat = deltaInList(biglat)
    deltaInlon = deltaInList(biglon)
    disturbancePoint = 0

    for j in range(len(biglat)):
        moyDeltaInLat.append(moyenne(deltaInlat[j], len(deltaInlat[j])))
        moyDeltaInLon.append(moyenne(deltaInlon[j], len(deltaInlon[j])))

    for j in range(1, len(moyDeltaInLat)):
            if moyDeltaInLat[j] > 0 and moyDeltaInLat[j + 1] > 0 and moyDeltaInLat[j - 1] < 0 and moyDeltaInLon[j] > 0:
                disturbancePoint = j - 2
            elif moyDeltaInLat[j] < 0 and moyDeltaInLon[j] > 0 and moyDeltaInLat[j + 1] == 0:
                disturbancePoint = j - 2
    return disturbancePoint

def convCompToPath(picComp,long_pas):
    Ax=[]
    Ay=[]
    xDist=[]
    yDist=[]

    # conversion en chemin
    for i in range(0, len(picComp) - 1):
        Ax.append(0)
        Ay.append(0)
    for i in range(1, len(picComp) - 1):
        Ax[i] = long_pas * sin(picComp[i - 1] * pi / 180) + Ax[i - 1]
        Ay[i] = long_pas * cos(picComp[i - 1] * pi / 180) + Ay[i - 1]

    for i in range(0, len(picComp) - 1):
        xDist.append(Ax[i])
        yDist.append(Ay[i])
    return xDist,yDist
def convCompToGPS(picComp,xDist,yDist,lon,lat):
    latInertie = []
    lonInertie = []
    latInFinal = []
    lonInFinal = []
    del_latInconnu = []
    del_lonInconnu = []
    gf = []
    degreelong = []

    #conversion en GPS
    for i in range(0,len(picComp)-1):
        latInertie.append(lat[0])
        lonInertie.append(lon[0])
    for  i in range(0, len(xDist) - 1):
        d = sqrt((xDist[i+1]- xDist[i])*(xDist[i+1]- xDist[i]) +(yDist[i+1]- yDist[i])*(yDist[i+1]- yDist[i]) )

        del_latInconnu.append(abs((d)/(1000*sqrt(1+tan((picComp[i]*3.14159/180))*tan((picComp[i]*3.14159/180)) ))))
        del_lonInconnu .append(abs(tan(picComp[i] * 3.14159 / 180)) * del_latInconnu[i])

        if (picComp[i]>= 0 and picComp[i]< 90):
            del_latInconnu[i] = del_latInconnu[i]
            del_lonInconnu[i] = del_lonInconnu[i]
        elif (picComp[i] >= 90 and picComp[i] < 180):
            del_latInconnu[i] = -del_latInconnu[i]
            del_lonInconnu [i]= del_lonInconnu[i]
        elif (picComp[i]>= 180 and picComp[i] < 270):
            del_latInconnu[i] = -del_latInconnu[i]
            del_lonInconnu[i] = -del_lonInconnu[i]
        elif (picComp[i]>= 270 and picComp[i] <= 360):
            del_latInconnu [i]= del_latInconnu[i]
            del_lonInconnu[i] = -del_lonInconnu[i]
        gf .append((3.14159 / 180) *latInertie[i])

        degreelong .append( 111 * cos(gf[i]))
        latInertie[i+1] = del_latInconnu[i] / 111 +latInertie[i]
        lonInertie[i+1] = del_lonInconnu[i] / degreelong[i] + lonInertie[i]
        latInFinal.append(latInertie[i])
        lonInFinal.append(lonInertie[i])
    return lonInFinal,latInFinal

#def assemblerGPStogpsInertie()

def compToGPS(lon,lat,xComp,tabAcce,biglon,biglat):
    finalLat=[]
    finalLon=[]

    moyLat = []
    moyLon = []

    nla = []
    nlon = []

    long_pas=0.75#m
    nbreDataParSec=50
    picIndices = detectionPic(tabAcce, nbreDataParSec, 28)
    picComp = relationPicComp(picIndices, xComp)

    disturbancePoint=moyDeltaInGps(biglon,biglat)
    ptTransition=disturbancePoint*nbreDataParSec
    pasTransition=[]

    for j in range(len(biglat)):
        moyLat.append(moyenne(biglat[j], len(biglat[j])))
        moyLon.append(moyenne(biglon[j], len(biglon[j])))
    for i in range(0, len(picIndices) - 1):
        if picIndices[i] < ptTransition:
            pasTransition.append(picIndices[i])

    picCompTransition = relationPicComp(picIndices[picIndices.index(pasTransition[-1]):-1], xComp)

     # conversion en chemin
    (xDist, yDist) = convCompToPath(picComp, long_pas)
    (xtr,ytr)= convCompToPath(picCompTransition, long_pas)

    #conversion en GPS
    (lonInFinal,latInFinal)=convCompToGPS(picComp, xDist, yDist, lon, lat)
    (lonIntr,latIntr)=convCompToGPS(picCompTransition, xtr, ytr, lon, lat)

    #Récupération de la partie non captée par le gps à l'aide de la boussole
    dernierBoutLat=[latInFinal[i] for i in range (len(moyLat),len(latInFinal))]
    dernierBoutLon = [lonInFinal[i] for i in range(len(moyLon), len(lonInFinal))]

    for j in range(0,len(dernierBoutLon)-1):
        nla.append(dernierBoutLat[j])
        nlon.append(dernierBoutLon[j])

    diflat=abs(nla[0]-moyLat[ disturbancePoint])
    diflon=abs(nlon[0]-moyLon[ disturbancePoint])
    diflattr = abs(latIntr[0] - lat[pasTransition[-1]])
    diflontr = abs(lonIntr[0] - lon[pasTransition[-1]])

    nlatr = [latIntr[i] - diflattr for i in range(0,len(latIntr)-1)]
    nlontr = [lonIntr[i] + diflontr for i in range(0,len(lonIntr)-1)]

    #Coller le GPS au gpsInertie(valeurs de la boussole converties en GPS)
    for i in range(0,len(nla)-1):
       if nla[i]> moyLat[disturbancePoint] and nlon[i]> moyLon[disturbancePoint]:
            nla=[nla[i]-diflat for i in range(len(nla))]
            nlon=[nlon[i]-diflon for i in range(len(nlon))]
       elif nla[i]< moyLat[disturbancePoint] and nlon[i]< moyLon[disturbancePoint]:
            nla=[nla[i]+diflat for i in range(len(nla))]
            nlon=[nlon[i]+diflon for i in range(len(nlon))]
       elif nla[i] > moyLat[disturbancePoint] and nlon[i] < moyLon[disturbancePoint]:
           nla = [nla[i] - diflat for i in range(len(nla))]
           nlon = [nlon[i] +diflon for i in range(len(nlon))]
       elif nla[i] < moyLat[disturbancePoint] and nlon[i] > moyLon[disturbancePoint]:
           nla = [nla[i]+diflat for i in range(len(nla))]
           nlon = [nlon[i] - diflon for i in range(len(nlon))]

    # Liste combinée finale
    for i in range(0,len(lat[0:pasTransition[-1]])):
        finalLat.append(lat[i])
        finalLon.append(lon[i])
    print(len(finalLat))
    for i in range(0,len(nlatr)-1):
        finalLat.append(nlatr[i])
        finalLon.append(nlontr[i])

    plt.figure()
    plt.plot(lon[0:-2],lat[0:-2],"b",label="latitude =f(longitude)")
    plt.plot(lonInFinal,latInFinal,"y",label="latitudeFromCompass =f(longitudeFromCompass)")
    #plt.plot(moyLon[0:  disturbancePoint], moyLat[0:  disturbancePoint], "g", label="moylatitude =f(moylongitude)", linewidth=1.5)
    #plt.plot(lon[0: ptTransition], lat[0:  ptTransition], "g", label="moylatitude =f(moylongitude)",linewidth=2)
    plt.plot(finalLon,finalLat,"r",label="latCompCombined =f(longCompCombined)")
    plt.plot(lonIntr,latIntr,label="transition")
    plt.xlabel('longitude')  # nom de l'axe x
    plt.ylabel('latitude')  # nom de l'axe y
    plt.legend()
    #plt.plot(nlonFinal, nla, "m")

    plt.show()



def valeur(bigxComplist, bigyComplist, bigzComplist, biglat, biglon, biglux,xComp,tabAcce,lat,lon):
    coteAdjascent1 = []
    coteOppose1 = []
    alpha1 = []

    moyXComplist= []
    moyYComplist = []
    moyZComplist = []
    moyDeltaInLat=[]
    moyDeltaInLon = []
    moyDeltaInLux = []
    moyLat=[]
    moyLon=[]
    moyLux=[]


    deltaXcomp=[]
    deltaYcomp = []
    deltaZcomp = []
    deltaLux=[]
    deltaLat=[]
    deltaLon=[]


    deltaInlat = deltaInList(biglat)
    deltaInlon = deltaInList(biglon)
    deltaInlux=deltaInList(biglux)
    stopPoint=0
    disturbancePoint=0
    tps=tempsList(xComplist)
    tpsAcce=tempsList(tabAcce)


    plt.figure()
    for j in range(0, len(biglon)):
        coteAdjascent1.append(biglon[j][-1] - biglon[j][0])
        coteOppose1.append(biglat[j][-1] - biglat[j][0])

    for j in range(0, len(coteAdjascent1)):
        if coteAdjascent1[j]!=0:
            alpha1.append(arctan((coteOppose1[j] / coteAdjascent1[j]) * pi / 180))



    for j in range(len(bigxComplist)):
        moyXComplist.append(moyenne(bigxComplist[j], len(bigxComplist[j])))
        deltaXcomp.append(bigxComplist[j][-1] - bigxComplist[j][0])
        moyYComplist.append(moyenne(bigyComplist[j], len(bigyComplist[j])))
        deltaYcomp.append(bigyComplist[j][-1] - bigyComplist[j][0])
        moyZComplist.append(moyenne(bigzComplist[j], len(bigzComplist[j])))
        deltaZcomp.append(bigzComplist[j][-1] - bigzComplist[j][0])
    for j in range(len(biglat)):

        moyLat.append(moyenne(biglat[j], len(biglat[j])))
        deltaLat.append(biglat[j][-1] - biglat[j][0])
        moyLon.append(moyenne(biglon[j], len(biglon[j])))
        deltaLon.append(biglon[j][-1] -biglon[j][0])
        moyLux.append(moyenne(biglux[j], len(biglux[j])))
        deltaLux.append(biglux[j][-1] - biglux[j][0])

        moyDeltaInLat.append(moyenne(deltaInlat[j], len(deltaInlat[j])))
        moyDeltaInLon.append(moyenne(deltaInlon[j], len(deltaInlon[j])))
        moyDeltaInLux.append(moyenne(deltaInlux[j], len(deltaInlux[j])))
        plt.plot(biglon[j], biglat[j],"y", linewidth=2.5)
        if deltaLat[j]==0 and deltaLat[j]==deltaLat[-1]==0 and  deltaLat[j - 1] != 0 :#and lux[j][i]>lux[j][i-1] :
                stopPoint=j

    for j in range(1, len(moyDeltaInLat)):
            if moyDeltaInLat[j] > 0 and moyDeltaInLat[j + 1] > 0 and moyDeltaInLat[j - 1] < 0 and moyDeltaInLon[j]>0:
                disturbancePoint = j-2
            elif moyDeltaInLat[j] < 0 and moyDeltaInLon[j]>0 and moyDeltaInLat[j + 1]== 0:
                disturbancePoint=j-2

    print( disturbancePoint)
    print(stopPoint)

    #plt.plot(moyLon[0:stopPoint], moyLat[0:stopPoint ],"b",label="Point d'arrêt", linewidth=4)
    #plt.plot(moyLon[0:  disturbancePoint], moyLat[0:  disturbancePoint],"g",label="Point de perturbation", linewidth=6)
    #plt.plot(moyLon, moyLat,label="Moyenne GPS", linewidth=2.5)


    #plt.legend()
    #plt.show()

    #plt.figure()
    #plt.plot(moyLat, "r")
    #plt.plot(moyLon, "b")
    #plt.plot(tpsAcce,tabAcce,"y")


    #________________________________________


    distDeparttoDisturbPt=gpsDist(lat,lon,0,disturbancePoint*50)
    picsIndices=detectionPic(tabAcce[ disturbancePoint*50:-1],50,28)
    distDisturbPointtoIn=(len(picsIndices) / 2) * 0.75
    distancetotale=distDeparttoDisturbPt+distDisturbPointtoIn

    picIndices=detectionPic(tabAcce,50,28)
    b=relationPicComp(picIndices,xComp)
    print (len(picIndices))

     #capAcceComp(b)
    #compDist(b)
    #compToGPS(b, lat, lon)


    print("distance totale parcourue", distancetotale)


    return  disturbancePoint

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
    #plt.figure("Real transition point")
    graphdata = plt.plot(longilist[0:longueur - 1], latlist[0:longueur2 - 1])  # tracer la courbe
    plt.xlabel('longitude')  # nom de l'axe x
    plt.ylabel('latitude')  # nom de l'axe y
    plt.legend()





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
    plt.legend()
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


#iO_index=pointInOut(latlist,longueur2)
#oI_index=pointOutIn(latlist,longueur2)



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


latintervalles = intervalles(latlist[0:-1], 300,50)  # jusqu'à -1 pour récupérer latlist jusqu'au dernier élément de type float
longiintervalles = intervalles(longilist[0:-1], 300, 50)
xCompIntervalles=intervalles(xComplistCalibree[0:-1], 300, 50)
yCompIntervalles=intervalles(yComplist[0:-1], 300, 50)
zCompIntervalles=intervalles(zComplist[0:-1], 300, 50)
luxIntervalles=intervalles(luxlist[0:-1],300,50)
acceIntervalles=intervalles(tabAcce[0:-1],300,50)
latliste2m = latlist2meter(latintervalles)
longilist2m = longilist2meter(latintervalles)


#valeur(xCompIntervalles,yCompIntervalles,zCompIntervalles, latintervalles ,longiintervalles,luxIntervalles,xComplistCalibree,tabAcce,latlist,longilist)
#print("xComplistCalibrée",xComplistCalibree)
compToGPS(longilist, latlist, xComplistCalibree, tabAcce, longiintervalles,  latintervalles)

#plt.figure('compass=f(t)')
plt.plot(tempsC[0:len(xComplist)-1],xComplist[0:len(xComplist)-1],label="xComp=f(t)")
plt.plot(tempsC[0:len(xComplist)-1],yComplist[0:len(xComplist)-1],label="yComp=f(t)")
plt.plot(tempsC[0:len(xComplist)-1],xComplistCalibree[0:len(xComplist)],label="xCompCalibree=f(t)")
plt.plot(tempsC[0:len(xComplist)-1],zComplist[0:len(xComplist)-1],label="zComp=f(t)")
plt.xlabel('temps (s)')                                                     #nom de l'axe x
plt.ylabel('Boussole (degrées)')                                                      #nom de l'axe y
plt.legend()
#plt.show()


print ("h",position2distancePoleNordM(48.52,7.74,84.826,-129.946))
print("g",gpsEnMetre2distanceGrandeListe(latintervalles,longiintervalles))
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

print ("dist",dist)
print("la distance parcourue dehors est",distance,"m")              #affichage de la distance parcourue
