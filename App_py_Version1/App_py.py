_author_="Massamba"

import numpy as np
import matplotlib.pyplot as plt


def read_light(filename):
    with open(filename, 'r') as f:
        for line in f:

            maliste = line.split(';')  # récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste);  # taille de la liste de départ

            for i in range(0, taille - 1):  # on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i]);  # on convertit en float
                taille = len(maliste);

            print(maliste[0:taille - 1])  # afficher la liste
            print("le nombre d'éléments de la liste du fichier %s" % filename, "est:%d " % taille)
            return maliste

 #La fonction pour ouvrir et créer la liste complete
def read(filename):
    with open(filename, 'r') as f:
        for line in f:

            maliste = line.split(';') #récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste); #taille de la liste de départ

            for i in range(0, taille - 1): #on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i]); #on convertit en float

            print(maliste[0:taille-1]) #afficher la liste
            print("le nombre d'éléments de la liste du fichier %s" % filename ,"est:%d "  % taille)
            return maliste



def delUnusedValues(L,b):
    l = []
    for i, j in enumerate(L):
     if j == b:
      l.append(i)
    return l


            #La fonction pour ouvrir et créer la liste sans les premiers zéros: s'applique aux données GPS
def read_gps(filename):
    with open(filename, 'r') as f:
        for line in f:
            maliste = line.split(';') #récupération des valeurs pour les mettre dans la liste maliste
            taille = len(maliste); #taille de la liste de départ
            i=0

            while i < taille - 1: #on parcourt le nombre d'éléments
                maliste[i] = float(maliste[i]); #on convertit en float


                if maliste[i] == 0:  #si la valeur de la liste =0 on supprime (del)
                   del (maliste[i])
                   i=0; #on revient en avant
                else: #sinon on avance d'un cran
                    i = i + 1;

                taille = len(maliste);# nouvelle taille de la liste

            print(maliste[0:taille-1]) #afficher la liste
            print("le nombre d'éléments de la liste du fichier %s" % filename ,"est:%d "  % taille)
            return maliste




#Appel de la fonction open qui lit les fichiers txt et les concatène dans une liste
#liste luxlist pour la lumière
luxlist=read_light("lightdata.txt");


#listes pour les données de l'accéléromètre
xlist=read("xdata.txt");
#ylist=read("ydata.txt");
#zlist=read("zdata.txt");

#xComplist=[];
#listes pour les données de la boussole
#yComplist=read("yCompdata.txt");
#zComplist=read("zCompdata.txt");
#xComplist=read("xCompdata.txt");



#liste latlist pour la latitude et liste longilist pour la latitude
latlist=read_gps("latdata.txt");
longilist=read_gps("longidata.txt");

#j=delUnusedValues(longilist,0)
#print(j)


#longilist=delUnusedValues(longilist)
longueur=len(longilist);
longueur2=len(longilist);


def limite(graphdata):

    plt.grid(True)

    xvalues = graphdata[0].get_xdata()
    yvalues = graphdata[0].get_ydata()
    xy = graphdata[0].get_xydata()
    i=0;
    o=0;
    l2 = list(range(len(xy)+1));
    for i,point in enumerate(xy):
        if xy[i][1]>1000.0 and xy[i][1]<2000.0:
            print(i,point)
            l2[o]=i
            o=o+1


    print(l2[0])

           #xvalues= graphdata[0].get_xdata()
          #""" k=xy[i][0]
           #print (xvalues)
           #print(k)"""


          if i ==l2[0]: #je dois mettre une valeur fixe
               # plt.plot(g[1], 'o')
               plt.plot(point[0],point[1],'o')
               plt.show();





graphlux=plt.plot(luxlist[0:longueur-1]);
j=limite(graphlux)


plt.grid(True)
graphGps=plt.plot(longilist[0:longueur-1],latlist[0:longueur2-1]);
k=limite(graphGps)

#xyg=graphGps[0].get_xydata()
#id=np.where(xyg==xyg[int(7.74113043)])
#print(id)

#plt.plot(zlist[0:longueur-1]);
plt.show();

#plt.plot(xlist[0:longueur-1]);
plt.show();







