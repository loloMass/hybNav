import matplotlib.pyplot as plt

import numpy as np

"""L = [[0, 2], [0,2],[3, 0]]

def index(e,L):

    for i, b in enumerate(L):
        l = []
        if e == b:
            del(b)
            l.append(i)
            return l
print(index([0,2], L))

m = [0, 0, 0, 0, 2, 2, 3, 4]

def delUnusedValues(L):
 l = []
 for i, j in enumerate(L):
    if j == 0:
     l.append(i)
 return l

p = delUnusedValues(m)
print(p)"""
m=[2,2,5,8,9,1,3,7]
n=[1,2,6,8,9]


def delUnusedValues(L,T ,b):
    o = 0;
    l = []
    nb=len(L)-len(T)
    b> nb
    for i in range(b, len(L)):
        if i < b and i> (b-nb):
            del(L[i])
            #L=L[b-nb:b-1:1]
        l.append(L[b])
        b=b+ 1

    print(l)
    print (b-nb)
    print(len(l))
    return l


delUnusedValues(m,n ,4)

def delate (bigList,smallList):
   n= len(bigList)-len(smallList)
   del(bigList[:n])
   print(m)
   return(m)
delate (m,n)

a = [1,2,3,4]
b = [5,6,7,8]

c = [a[i]*b[i]*b[i] for i in range(len(a))]
print(c)

L = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
luxlist=[ 8740.0, 8741.0, 8742.0, 8743.0, 8667.0, 8667.0, 8665.0, 8666.0, 8667.0, 8668.0, 8669.0, 8670.0, 8671.0, 8672.0, 8667.0, 8667.0]

"""print (luxlist)
o = 0;
l = list(range(len(luxlist)));
for i, point in enumerate(luxlist):
        l[o] = i
        o = o + 1
print (len(l))
print (l)"""


def tempsList(liste):
    tps=[]
    for x in range (0, len(liste)):
        x=x*0.02                                         #conversion du nombre d'éléments en seconde
        tps.append(x)
    #print(tps)
    return tps
def max(t):
    listePic = []
    for j in range(0, len(t) - 1):
         for n in range(0, 2):
            if t[j - n] < t[j] and t[j + n] < t[j] and  (t[j-2]%(t[j]%2))<1:
                print("on a un maximum en %d" % j)
                listePic.append(j)
                return listePic

def intervalle(liste):
    for i,elt in enumerate(liste):
        if i % 4  == 0 :
            t = liste[i:i + 10]
            print(t)
            return t

def plotMax(liste):

    temps = tempsList(liste)
    plt.figure("test")
    graph = plt.plot(temps[0:len(liste) - 1], liste[0: len(liste) - 1])
    pt = graph[0].get_xydata()
    t=intervalle(liste)
    pic=max(t)

    for k, p in enumerate(pt):
        for k1, p1 in enumerate(pic):
            if k == p1:  # si l'indice k est égale à l'indice j du point de transition
                plt.plot(pt[k][0], pt[k][1], 'o')




newGraph = plotMax(luxlist)

plt.show();




"""
for elt in maliste:
    for i in range (0,len(luxlist)-1):

        if elt==i:
            piclist.append(luxlist[i])
print (piclist)"""
