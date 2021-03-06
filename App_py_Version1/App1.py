_author_="Massamba"

import numpy as np
import matplotlib.pyplot as plt
from math import *

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
yComplist=newLength(yComplist,longilist,'yComplist')
zComplist=newLength(zComplist,longilist,'zComplist')



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
for i in range (0, longueur-1):
    d=xlist[i]*xlist[i]+ylist[i]*ylist[i]+zlist[i]*zlist[i]
    j=sqrt(d)
    tabAcce.append(j)
print ("tabAcce",tabAcce)


plt.figure('accélérometre=f(t)')
plt.plot(temps[0:longueur - 1], xlist[0:longueur - 1], label="x=f(t)");
plt.plot(temps[0:longueur - 1], ylist[0:longueur - 1], label="y=f(t)");
plt.plot(temps[0:longueur - 1], zlist[0:longueur - 1], label="z=f(t)");
plt.plot(temps[0:longueur - 1], tabAcce[0:longueur - 1], label="vecteurAcceleromètre=f(t)");
plt.xlabel('temps (s)')                                              # nom de l'axe x
plt.ylabel('Accélération (m/s²)')                                          # nom de l'axe y
plt.legend();
plt.show();


#tracé de la courbe générale de l'accéléromètre en fonction du temps en calculant le module des valeurs





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

def intervalle (liste,n,diviseur):
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

NewListe = intervalle(tabAcce,50,28)                                           #NewListe est la liste des intervalles
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
            if (elt[i]-elt[i+1]) <=200 and  (elt[i]-elt[i+1])>0 and elt[i+1]<2000 :
                b.append(elt[i+1])



    return b

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

def reaLimitOutIn(graphdata,liste):
    x=[]
    y=[]
    plt.grid(True)
    xy = graphdata[0].get_xydata()                          #liste de tous les points de la courbes de coordonnées x et y
    p=luxlist.index(785)
    p1=luxlist.index(15813)


    print("p",p,"p1",p1,"x",x)
    #x=xy[0][99.2098:103.108]
    plt.figure("Real transition point")
    graphdata = plt.plot(temps[0:len(liste) - 1], luxlist[0:len(liste) - 1], label="light=f(t)") # tracer la courbe
    v=temps[4624:5149]
    for i,elt in enumerate(v):
        print("elt",elt)
        print("i",i)
        print(v[0])
        print(v[-2])
        a=((785-15813)/( v[-2] -v[0]))
        print("a",a)

        y.append(a*elt+( 15813-a*v[0]))
    print ("y",y)
    plt.plot(temps[4624:5149], y, label="light=f(t)")
    plt.xlabel('temps (s)')  # nom de l'axe x
    plt.ylabel('light (lux)')  # nom de l'axe y
    plt.legend();
    o=0;

    l = list(range(len(xy)+1));
    nb=[]

    for i,point in enumerate(xy):                           #On parcourt les points de xy d'indice i
            l[o]=point[1]
            o=o+1

    oI_index = pointOutIn(latlist, longueur2)
    inter= intervalle(l,100,56)
    b = seuil(inter)

    for indice,elt in enumerate(b):
        if b.count(elt) > 1:
            b.remove(elt)
    for indice, elt in enumerate(b):
        if elt == luxlist[oI_index]:
            nb = b[indice:indice + len(b)]



    for j, e in enumerate(xy):
        for i,elt in enumerate (nb):
                if e[1]== nb[0]:
                     plt.plot(xy[j][0],xy[j][1],'X')
                    # plt.plot(temps[0:longueur - 1], xy[0:longueur - 1], label="y");

    plt.show()


    """for j, elt in enumerate(b):
            if b.count(elt) > 1:
                b.remove(elt)"""
    #print (b.index(luxlist[oI_index]))
    print("nb",len( nb))
    print(b)
    print(len(b))
    return nb



m=reaLimitOutIn(graphlux, luxlist)
print("m",m)



iO_index=pointInOut(latlist,longueur2)
oI_index=pointOutIn(latlist,longueur2)



#print (luxlist[oI_index])

 #tracé des courbes de la boussole
#tempsComp=tempsList(xComplist)
plt.figure('compass=f(t)')
plt.plot(temps[0:longueur-1],xComplist[0:longueur-1],label="xComp=f(t)");
plt.plot(temps[0:longueur-1],yComplist[0:longueur-1],label="yComp=f(t)");
plt.plot(temps[0:longueur-1],zComplist[0:longueur-1],label="zComp=f(t)");
plt.xlabel('temps (s)')                                                     #nom de l'axe x
plt.ylabel('Boussole')                                                      #nom de l'axe y
plt.legend() ;
#plt.show();


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
