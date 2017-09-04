_author_ = "Massamba"


# Déclaration des bibliothèques utilisées

import numpy as np #Pour les algorithmes mathématiques
import matplotlib.pyplot as plt #Pour l'affichage des courbes
from math import *  #Pour les formules mathématiques
from pylab import *

#Instanciation des listes utilisées

tabAcce = []  #Récupère le vecteur d'accélération
multiple28 = []  #Récupère la liste des multiples de 28
indicesPics = []  #Récupère la liste des indices des pics
pic = []
picValues = []    #Récupère la valeur de l'accélération au niveau des pics


# fonction qui converti la taille des autres listes en fonction de celles du GPS en utilisant la taille des listes de longitude et de latitude
#Le but est d'éliminer les valeurs inutiles au début de l'acquisition des données du GPS et faire le traitement sur des liste de même taille

def newLength(bigList, smallList, nomListe): #Bigliste= liste de longitude ou latitude et smallList :la liste à réduire
    n = len(bigList) - len(smallList)  #n la différence de taille des listes
    del (bigList[:n])                   #On élime du début jusqu'à n
    lenBigList = len(bigList)
    print("le Nouveau nombre d'éléments de la liste du fichier %s" % nomListe, "est:%d  " % lenBigList) #affichage de la taille et de la nouvelle liste
    return (bigList)

# La fonction pour lire le fichier texte et créer la liste complete

def read(filename):
    with open(filename, 'r') as f:
        for line in f:

            maliste = line.split(';')  # récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste)  # taille de la liste de départ

            for i in range(0, taille - 1):  # on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i])  # on convertit en float

                # print(maliste[0:taille-1]) #afficher la liste
                # print("le nombre d'éléments de la liste du fichier %s" % filename ,"est:%d "  % taille)
            return maliste

# La fonction pour lire les fichiers texte des données du GPS et créer la liste sans les premiers zéros (éléments inutiles): s'applique aux données GPS

def read_gps(filename):
    with open(filename, 'r') as f:
        for line in f:
            maliste = line.split(';')  # récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste)  # taille de la liste de départ
            i = 0

            while i < taille - 1:  # on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i])  # on convertit en float

                if maliste[i] == 0:  # si la valeur de la liste =0 on supprime (del)
                    del (maliste[i])
                    i = 0  # on revient en avant
                else:  # sinon on avance d'un cran
                    i = i + 1
                taille = len(maliste)  # nouvelle taille de la liste

                # print(maliste[0:taille-1])                  #afficher la liste
                # print("le nombre d'éléments de la liste du fichier %s" % filename ,"est:%d "  % taille)
            return maliste

# définition du temps pour tracer les courbes de l'accélération, de la lumière et de la boussole en fonction du temps

def tempsList(liste): #prend en paramètre la liste de données
    tps = []
    for x in range(0, len(liste)):
        x = x * 0.02  # conversion du nombre d'éléments en seconde
        tps.append(x)
    # print(tps)
    return tps


# Appel des fonctions read et read_gps qui lisent les fichiers txt et les concatènent dans une liste


# listes pour les données de l'accéléromètre
xlist = read("xdata.txt")
ylist = read("ydata.txt")
zlist = read("zdata.txt")

# listes pour les données de la boussole
xComplist = read("xCompdata.txt")
yComplist = read("yCompdata.txt")
zComplist = read("zCompdata.txt")

# liste "latlist" pour la latitude et liste "longilist" pour la latitude
latlist = read_gps("latdata.txt")
longilist = read_gps("longidata.txt")
longueur = len(longilist)   #On récupère la longueur des listes de longitude et de latitude
longueur2 = len(latlist)

# liste "luxlist" pour la lumière
luxlist = read("lightdata.txt")

# Conversion des listes pour les adapter à la taille des listes GPS (latitude et longitude)
#Appel de la fonction newLength

luxlist = newLength(luxlist, longilist, 'luxlist')
xlist = newLength(xlist, longilist, 'xlist')
ylist = newLength(ylist, longilist, 'ylist')
zlist = newLength(zlist, longilist, 'zlist')
xComplist = newLength(xComplist, longilist, 'xComplist')
"""yComplist=newLength(yComplist,longilist,'yComplist')
zComplist=newLength(zComplist,longilist,'zComplist')"""


# Calcul du vecteur d'accélération

for i in range(0, longueur - 1):
    d = xlist[i] * xlist[i] + ylist[i] * ylist[i] + zlist[i] * zlist[i]
    j = sqrt(d)  #Norme des trois vecteurs de l'accéléromètre
    tabAcce.append(j)
print("tabAcce", tabAcce)  #Affichage de la liste

#Fonction pour calibrer (mettre à jour les données de la boussole (+360° sur les valeur négatives))
def calibrageBoussole(liste):
    listeCalibree = []
    for i in range(0, len(liste) - 1):
        if liste[i] < 0:
            listeCalibree.append(liste[i] + 360)
        elif liste[i] > 0:
            listeCalibree.append(liste[i])
        elif liste[i] == 0:
            listeCalibree.append(liste[i])
    return listeCalibree

#Fonction " somme"

def somme(UneListe, taille):
    compteur = 0
    accumulateur = 0
    while compteur < taille:
        accumulateur += UneListe[compteur]
        compteur += 1
    return accumulateur


# Fonction "moyenne"

def moyenne(UneListe, taille):
    return somme(UneListe, taille) / len(UneListe)

#DETECTION DE PICS________________________________

# Création d'une grande liste récupérant les Intervalles d'analyse (Sous listes de données)

def intervalles(liste, n, diviseur): #n est le nombre de données de l'intervalle d'analyse et diviseur l'indice de l'intervalle d'analyse à partir duquel on construit l'intervalle suivant
    return [liste[x:x + n] for x, elt in enumerate(liste) if x % diviseur == 0]

# Fonction qui récupère les intervalles d'analyse afin de distinguer les valeurs maximales d'accélération (Pics=pas) selon les conditions

def maxi(t):  #t est un intervalle d'analyse qui contient les valeurs de l'accélération
    l = []
    p = []
    acce_zero = moyenne(t, len(t))
    for n in range(1, 11):
        for j, x in enumerate(t[len(t) - 39:len(t) - 11]):
            if t[j] > t[j + n] and t[j] > t[j - n] and t[j] > acce_zero + 2.5: #Conditions de distinction des pics
                l.append(j)

        return l

# ___________________________________________________________________________Gestion des pics



def detectionPic(listeOriginale, k, diviseur):
    L = [listeOriginale[x:x + k] for x, elt in enumerate(listeOriginale) if x % diviseur == 0]
    T = [maxi(L[i]) for i in range(0, len(L))]
    picsValues = []
    realIndicePics = []
    finalIndicesPics = []
    tps = tempsList(listeOriginale)
    longueur = len(listeOriginale)
    plt.figure()
    grapheAcce = plt.plot(tps[0:longueur - 1], listeOriginale[0:longueur - 1], label="accelerometer=f(t)")
    indicesAcce = grapheAcce[0].get_xydata()
    multipl28 = [y for y, elt in enumerate(listeOriginale) if y % diviseur == 0]
    NL = []
    for i in range(0, len(T)):
        for j, elt in enumerate(T[i]):
                realIndicePics.append(elt + multipl28[i])

    for k1 in range(0, len(realIndicePics) - 1):
            picsValues.append(listeOriginale[realIndicePics[k1]])

            if realIndicePics[k1 + 1] - realIndicePics[k1] > 5 and listeOriginale[realIndicePics[k1]] > listeOriginale[
                realIndicePics[k1 + 1]]:
                finalIndicesPics.append(realIndicePics[k1])
            elif realIndicePics[k1 + 1] - realIndicePics[k1] > 5 and listeOriginale[realIndicePics[k1]] < \
                    listeOriginale[
                        realIndicePics[k1 + 1]]:
                finalIndicesPics.append(realIndicePics[k1 + 1])
            elif realIndicePics[k1 + 1] - realIndicePics[k1] < 5 and listeOriginale[realIndicePics[k1]] > \
                    listeOriginale[
                        realIndicePics[k1 + 1]]:
                finalIndicesPics.append(realIndicePics[k1])
            elif realIndicePics[k1 + 1] - realIndicePics[k1] > 5 and listeOriginale[realIndicePics[k1]] < \
                    listeOriginale[
                        realIndicePics[k1 + 1]]:
                finalIndicesPics.append(realIndicePics[k1 + 1])

    for j in range(0, len(finalIndicesPics) - 1):
            if finalIndicesPics[j] != finalIndicesPics[j + 1] and finalIndicesPics[j + 1] - finalIndicesPics[j] > 15:
                NL.append(finalIndicesPics[j])

    # Tracé des pics
    for k, p in enumerate(listeOriginale):
            for k1, pt in enumerate(NL):
                if k == pt:
                    plt.plot(indicesAcce[k][0], indicesAcce[k][1], 'X')
    plt.ylabel('accélération en m/s²')  # nom de l'axe x
    plt.xlabel('temps en s')
    plt.legend()
    plt.show()

    return NL
# ___________________________________________________________________________Détection de la perturbation

#Fonction qui calcule la distance parcourue à partir des coordonnées GPS en entrant le point de départ "dep" et le point d'arrivée "arr"
#Elle prend aussi en paramètre les listes des coordonnées GPS

def gpsDist(latitudeListe, longitudeListe, dep, arr):
    dist = 6378 * 1000 * acos(
        sin((latitudeListe[dep] * pi) / 180) * sin((latitudeListe[arr] * pi) / 180) +
        cos((latitudeListe[dep] * pi) / 180) * cos((latitudeListe[arr] * pi) / 180) *
        cos((longitudeListe[arr] * pi) / 180 - (longitudeListe[dep] * pi) / 180))
    return dist #distance en mètres

#Fonction qui calcule la distance parcourue à partir des coordonnées GPS sur chaque intervalle d'analyse
#Elle prend aussi en paramètre les listes des intervalles d'analyse contenant les coordonnées GPS

def gpsEnMetre2distanceGrandeListe(latitudeListe, longitudeListe):
    dist = []
    for j in range(0, len(latitudeListe) - 1):
        dist.append(6378 * 1000 * acos(
            sin((latitudeListe[j][0] * pi) / 180) * sin((latitudeListe[j][-1] * pi) / 180) +
            cos((latitudeListe[j][0] * pi) / 180) * cos((latitudeListe[j][-1] * pi) / 180) *
            cos(((longitudeListe[j][-1] * pi) / 180) - ((longitudeListe[j][0] * pi)) / 180)))

    return dist #distance en mètres

#Fonction qui calcule le delta entre deux valeurs consécutives dans un intervalle d'analyse et renvoie dans une liste des sous-listes contenant ces delta
def deltaInList(list):
    L = [(list[j][i] - list[j][i - 1]) for j in range(0, len(list)) for i in range(1, len(list[j]))]
    taille = [len(elt) - 1 for elt in list]
    finalList = []
    prev = 0

    for i, index in enumerate(taille):
        finalList.append(L[prev:prev + index])

        prev = prev + index
    return finalList

# METHODES UTILISEES

#Méthode VARIATIONS DE LA LUMIERE

def seuil(L):  # fonction pour déterminer les points de luxlist pendant l'entrée au niveau de la porte
    b = []
    for elt in L:
        for i in range(0, len(elt) - 1):
            if (elt[i] - elt[i + 1]) > 0 and elt[i + 1] < 1000:
                return elt[i + 1]


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


def reaLimitOutIn(graphdata, luxliste):

    xy = graphdata[0].get_xydata()  # liste de tous les points de la courbe de la lumière de coordonnées x et y
    graphdata = plt.plot(temps[0:len(luxliste) - 1], luxlist[0:len(luxliste) - 1], label="light=f(t)")  # tracer la courbe
    plt.xlabel('temps (s)')  # nom de l'axe x
    plt.ylabel('light (lux)')  # nom de l'axe y
    plt.legend();
    l = []
    graphListe = []

    for i, point in enumerate(luxliste):  # On parcourt les points de xy d'indice i
        l.append(point)
    oI_index = pointOutIn(latlist, longueur2)
    inter = intervalles(l, 300, 50)
    b = seuil(inter)


    for j, elt in enumerate(luxliste):
        if elt == b:
            graphListe = luxliste[luxliste.index(elt):oI_index]

    #print("graphliste", graphListe)

    for j, e in enumerate(xy):
        for i, elt in enumerate(graphListe):
            if e[1] == elt:
                plt.plot(xy[j][0], xy[j][1], 'X')

    plt.show()
    return b


#Méthode ECART ET PROJECTION DES DONNEES

def axPlusb(x, a, b):
    L = [a[j] * x[j][i] + b[j] for j in range(len(x)) for i in range(0, len(x[j]))]
    taille = [len(elt) for elt in x]
    output = []
    prev = 0

    for i, index in enumerate(taille):
        output.append(L[prev:prev + index])
        prev = prev + index

    return output
def projection(x, y, a, b):
    L = [(abs((-a[j]) * x[j][i] + y[j][i] - b[j]) / sqrt(a[j] ** 2 + 1)) for j in range(len(x)) for i in
         range(0, len(x[j]))]
    taille = [len(elt) for elt in x]
    deviationBetween2graph = []
    prev = 0

    for i, index in enumerate(taille):
        deviationBetween2graph.append(L[prev:prev + index])

        prev = prev + index
    return deviationBetween2graph


def ecartType(latList, longiList):
    plt.grid(True)
    # _______ tracé des droites d'équation latitude= a* longitude + b
    newLongiValues = []
    newLatValues = []
    a = []
    b = []
    latIntervalles = intervalles(latList[0:-1], 300, 50)  # jusqu'à -1 pour récupérer latlist jusqu'au dernier élément de type float
    longiIntervalles = intervalles(longiList[0:-1], 300, 50)

    for i, elt in enumerate(latIntervalles):
        if (longiIntervalles[i][-1] - longiIntervalles[i][0]) != 0:  # On élimine les cas de division par zéro
            a.append(
                (latIntervalles[i][-1] - latIntervalles[i][0]) / (longiIntervalles[i][-1] - longiIntervalles[i][0]))
            b.append(latIntervalles[i][0] - a[i] * longiIntervalles[i][0])
            newLongiValues.append(longiIntervalles[i])  # La nouvelle liste de valeurs longitudinales de même taille que la liste des coefficients a et b
            newLatValues.append(latIntervalles[i])  # La nouvelle liste de valeurs de latitude de même taille que la liste des coefficients a et b

    y = axPlusb(newLongiValues, a, b)  # y= a*x+b avec x la liste des valeurs de  longitude ici newLongiValues

    for i in range(0, len(newLongiValues)):
        plt.plot(newLongiValues[i], y[i])  # Affichage de y en fonction de newLongiValues y= a* newLongiValues + b
        plt.plot(newLongiValues[i], newLatValues[i], 'r', linewidth=2.5)
        plt.plot(longiIntervalles[i], latIntervalles[i], 'r', linewidth=2.5)

    plt.xlabel('longitude')  # nom de l'axe x
    plt.ylabel('latitude')  # nom de l'axe y
    plt.legend()
    plt.show()

    # _______calcul d'écart  entre chaque point de la courbe d'origine et les différentes droites

    ecart = projection(newLongiValues, newLatValues, a, b) #Retourne la valeur de la différence entre les coordonnées GPS et les droites d'équation y=a*x+b passant par les deux extrémités de l'intervalle
    print("écart", ecart)
    return y


#Méthode DISTANCE EVOLUTIVE

def deltaInDistGrandeListe(longitudeListe, latitudeListe):
    taille = [5 for elt1 in latitudeListe]
    finalList = []
    prev = 0
    prev2 = 0
    listeBinaire = []
    listeB = []
    indiceTr = []
    moylisteB = []
    disturbancePoint=0
    moyDeltaInLat = []
    moyDeltaInLon = []
    deltaInlat = deltaInList(latitudeListe)
    deltaInlon = deltaInList(longitudeListe)

    for j in range(len(latitudeListe)): #Moyenne de latitude et de longitude
        moyDeltaInLat.append(moyenne(deltaInlat[j], len(deltaInlat[j])))
        moyDeltaInLon.append(moyenne(deltaInlon[j], len(deltaInlon[j])))

    deltaIndist = [6378 * 1000 * acos(
        sin((latitudeListe[i][0] * pi) / 180) * sin((latitudeListe[i][j] * pi) / 180) +
        cos((latitudeListe[i][0] * pi) / 180) * cos((latitudeListe[i][j] * pi) / 180) *
        cos(((longitudeListe[i][j] * pi) / 180) - ((longitudeListe[i][0] * pi) / 180))) for i in
                   range(0, len(latitudeListe) - 1) for j in range(50, len(latitudeListe[i])) if
                   j % 50 == 0 and j is not 0] #On calcule le delta (la différence) entre deux valeurs consécutives de distance dans chaque intervale de 6 secondes

    # mettre les distances dans une liste de liste
    for i, index in enumerate(taille):
        finalList.append(deltaIndist[prev:prev + index])
        prev = prev + index

    # conditions pour déterminer si la distance augmente ou diminue
    taille2 = [len(elt) - 1 for elt in finalList]
    for i, elt in enumerate(finalList):
        for j in range(0, len(elt) - 1):
            if elt[j + 1] - elt[j] >= 0:
                listeBinaire.append(1) #Si la distance augmente listeBinaire =1 sinon 0
            else:
                listeBinaire.append(0)

    for i, index in enumerate(taille2):  #On créé une liste contenant les listes binaires correspondants à chaque intervalle d'analyse de départ
        listeB.append(listeBinaire[prev2:prev2 + index])
        prev2 = prev2 + index

    # détection de la perturbation
    for j in range(0, len(listeB)):
        if len(listeB[j]) != 0:
            moylisteB.append(moyenne(listeB[j], len(listeB[j]))) #On calcule la moyenne sur chaque intervalle de liste binaire
    for i in range(0, len(moylisteB) - 1):
        if moylisteB[i] < 1 and moylisteB[i + 1] < 1 and moylisteB[i + 2] < 1 and moylisteB[i + 3] < 1: #condition pour non-perturbation
            indiceTr.append(i * 50)

    for j in range(1, len(moylisteB)):

            if moyDeltaInLat[j] < 0 and moyDeltaInLon[j] > 0 and moyDeltaInLat[j + 1] == 0:
                disturbancePoint = (j - 2)*50
            elif moyDeltaInLat[j] > 0 and moyDeltaInLat[j + 1] > 0 and moyDeltaInLat[j - 1] < 0 and moyDeltaInLon[j] > 0:
                disturbancePoint = indiceTr[0]
            elif moylisteB[j] < 1 and moylisteB[j + 1] < 1 and moylisteB[j + 2] < 1 and moylisteB[j + 3] < 1:
                disturbancePoint = indiceTr[0]
    #print("tr", len(listeB), len(finalList), len(moylisteB), len(deltaIndist))
    print("tr", len(moylisteB), len(moyDeltaInLat))
    #print(moylisteB, indiceTr)
    return disturbancePoint

#Méthode MOYENNE ENTRE DEUX VALEURS CONSECUTIVES DES DONNEES GPS

def moyDeltaInGps(biglon, biglat): #En entrées les listes de sous-listes (intervalles d'analyses) du GPS
    moyDeltaInLat = []
    moyDeltaInLon = []
    deltaInlat = deltaInList(biglat)
    deltaInlon = deltaInList(biglon)
    disturbancePoint = 0

    for j in range(len(biglat)): #moyenne sur chaque intervales des delta (différence entre deux coordonées consécutives)
        moyDeltaInLat.append(moyenne(deltaInlat[j], len(deltaInlat[j])))
        moyDeltaInLon.append(moyenne(deltaInlon[j], len(deltaInlon[j])))

    for j in range(1, len(moyDeltaInLat)):
        if moyDeltaInLat[j] > 0 and moyDeltaInLat[j + 1] > 0 and moyDeltaInLat[j - 1] < 0 and moyDeltaInLon[j] > 0:
            disturbancePoint = j - 2
        elif moyDeltaInLat[j] < 0 and moyDeltaInLon[j] > 0 and moyDeltaInLat[j + 1] == 0:
            disturbancePoint = j - 2

    return disturbancePoint #retourne le point du début de la perturbation

# ___________________________________________________________________________GPS INERTIEL

# Détermination des delta_longitude et delta_latitude en mètres à partir de la centrale inertielle
def convCompToPath(picComp, long_pas):
    Ax = []
    Ay = []
    xDist = []
    yDist = []


    for i in range(0, len(picComp) - 1):
        Ax.append(0)
        Ay.append(0)
    for i in range(1, len(picComp) - 1):
        Ax[i] = long_pas * sin(picComp[i - 1] * pi / 180) + Ax[i - 1]
        Ay[i] = long_pas * cos(picComp[i - 1] * pi / 180) + Ay[i - 1]

    for i in range(0, len(picComp) - 1):
        xDist.append(Ax[i])
        yDist.append(Ay[i])
    return xDist, yDist

#Conversion en degrés du GPS inertiel

def convCompToGPS(picComp, xDist, yDist, lon, lat):
    latInertie = []
    lonInertie = []
    latInFinal = []
    lonInFinal = []
    del_latInconnu = []
    del_lonInconnu = []
    gf = []
    degreelong = []

    # conversion en GPS
    for i in range(0, len(picComp) - 1):
        latInertie.append(lat[0])
        lonInertie.append(lon[0])
    for i in range(0, len(xDist) - 1):
        d = sqrt((xDist[i + 1] - xDist[i]) * (xDist[i + 1] - xDist[i]) + (yDist[i + 1] - yDist[i]) * (
        yDist[i + 1] - yDist[i]))

        del_latInconnu.append(
            abs((d) / (1000 * sqrt(1 + tan((picComp[i] * 3.14159 / 180)) * tan((picComp[i] * 3.14159 / 180))))))
        del_lonInconnu.append(abs(tan(picComp[i] * 3.14159 / 180)) * del_latInconnu[i])

        if (picComp[i] >= 0 and picComp[i] < 90):
            del_latInconnu[i] = del_latInconnu[i]
            del_lonInconnu[i] = del_lonInconnu[i]
        elif (picComp[i] >= 90 and picComp[i] < 180):
            del_latInconnu[i] = -del_latInconnu[i]
            del_lonInconnu[i] = del_lonInconnu[i]
        elif (picComp[i] >= 180 and picComp[i] < 270):
            del_latInconnu[i] = -del_latInconnu[i]
            del_lonInconnu[i] = -del_lonInconnu[i]
        elif (picComp[i] >= 270 and picComp[i] <= 360):
            del_latInconnu[i] = del_latInconnu[i]
            del_lonInconnu[i] = -del_lonInconnu[i]
        gf.append((3.14159 / 180) * latInertie[i])

        degreelong.append(111 * cos(gf[i]))
        latInertie[i + 1] = del_latInconnu[i] / 111 + latInertie[i]
        lonInertie[i + 1] = del_lonInconnu[i] / degreelong[i] + lonInertie[i]
        latInFinal.append(latInertie[i])
        lonInFinal.append(lonInertie[i])
    return lonInFinal, latInFinal

#_____________________________________________________Continuité du signal: GPS + GPS inertiel

#Fonction qui récupère la valeur de la boussole en degrés au niveau des pics
def relationPicComp(indPics, valComp):
    relPicComp = []
    for i, elt in enumerate(indPics):
        relPicComp.append(valComp[elt])
    return relPicComp

# def assemblerGPStogpsInertie()

def compToGPS(lon, lat, xComp, tabAcce, biglon, biglat):
    finalLat = []
    finalLon = []

    moyLat = []
    moyLon = []

    nla = []
    nlon = []

    long_pas = 0.75  # m
    nbreDataParSec = 50
    picIndices = detectionPic(tabAcce, nbreDataParSec, 28)
    picComp = relationPicComp(picIndices, xComp)

    disturbancePoint = moyDeltaInGps(biglon, biglat)
   #ptTransition = deltaInDistGrandeListe(biglon, biglat) #Formule si on utilise la fonction distance évolutive
    ptTransition = disturbancePoint * nbreDataParSec
    pasTransition = []

    for j in range(len(biglat)):
        moyLat.append(moyenne(biglat[j], len(biglat[j])))
        moyLon.append(moyenne(biglon[j], len(biglon[j])))
    for i in range(0, len(picIndices) - 1):
        if picIndices[i] < ptTransition:
            pasTransition.append(picIndices[i])
    print("r",pasTransition)
    print (ptTransition)
    print(len(lat[0:-1]))

    picCompTransition = relationPicComp(picIndices[picIndices.index(pasTransition[-1]):-1], xComp)

    # conversion en chemin
    (xDist, yDist) = convCompToPath(picComp, long_pas)
    (xtr, ytr) = convCompToPath(picCompTransition, long_pas)

    # conversion en GPS
    (lonInFinal, latInFinal) = convCompToGPS(picComp, xDist, yDist, lon, lat)
    (lonIntr, latIntr) = convCompToGPS(picCompTransition, xtr, ytr, lon, lat)

    # Récupération de la partie non captée par le gps à l'aide de la boussole
    diflattr = abs(latIntr[0] - lat[pasTransition[-1]])
    diflontr = abs(lonIntr[0] - lon[pasTransition[-1]])

    nlatr = [latIntr[i] - diflattr for i in range(0, len(latIntr) - 1)]
    nlontr = [lonIntr[i] + diflontr for i in range(0, len(lonIntr) - 1)]

    # Liste combinée finale
    for i in range(0, len(lat[0:pasTransition[-1]])):
        finalLat.append(lat[i])
        finalLon.append(lon[i])
    print(len(finalLat))
    for i in range(0, len(nlatr) - 1):
        finalLat.append(nlatr[i])
        finalLon.append(nlontr[i])

    #t=deltaInDistGrandeListe(biglon, biglat)
    plt.figure()
    plt.plot(lon[0:-2], lat[0:-2], "r", label="latitude =f(longitude)")
    # plt.plot(lon[0:t], lat[0:t], "g", label="latitude jusqu'au point de perturbation =f(longitude jusqu'au point de perturbation )",linewidth=2)
    plt.plot(lonInFinal,latInFinal,"y",label="latitudeFromCompass =f(longitudeFromCompass)")
    plt.plot(lon[0: ptTransition], lat[0:  ptTransition], "g", label="latitude jusqu'au point de perturbation =f(longitude jusqu'au point de perturbation", linewidth=2)
    plt.plot(finalLon,finalLat,"r",label="latCompCombined =f(longCompCombined)")
    # plt.plot(lonIntr,latIntr,label="transition")
    # plt.plot(moyLon,moyLat,"g",label="moyLatitude =f(moyLongitude)")
    plt.xlabel('longitude')  # nom de l'axe x
    plt.ylabel('latitude')  # nom de l'axe y
    plt.legend()
    plt.show()

    return finalLon, finalLat

#_____________________________________________Application


#Instanciation des paramètres pour l'appel des fonctions de détection de la perturbation du GPS à l'entrée des bâtiments

#Calibration de la boussole
xComplistCalibree = calibrageBoussole(xComplist)

#Création des intervalles d'analyse
latintervalles = intervalles(latlist[0:-1], 300, 50)  # jusqu'à -1 pour récupérer latlist jusqu'au dernier élément de type float
longiintervalles = intervalles(longilist[0:-1], 300, 50)
xCompIntervalles = intervalles(xComplistCalibree[0:-1], 300, 50)
yCompIntervalles = intervalles(yComplist[0:-1], 300, 50)
zCompIntervalles = intervalles(zComplist[0:-1], 300, 50)
luxIntervalles = intervalles(luxlist[0:-1], 300, 50)
acceIntervalles = intervalles(tabAcce[0:-1], 300, 50)

temps = tempsList(luxlist)
graphlux = plt.plot(temps[0:len(luxlist) - 1], luxlist[0:len(luxlist) - 1], label="light=f(t)")
reaLimitOutIn(graphlux, luxlist) #Méthode variation de la lumière
ecartType(latlist, longilist) #Méthode écart et projection des données
compToGPS(longilist, latlist, xComplistCalibree, tabAcce, longiintervalles, latintervalles) #Méthode des moyenne des delta-GPS sous couvert de la méthode de la distance évolutive
