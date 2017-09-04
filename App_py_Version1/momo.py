
import matplotlib.pyplot as plt
from math import *
from pylab import *

L = [9.39288120795659, 9.47330015508797, 9.563337211083594, 9.596164387241995, 9.456182709602173, 9.391865843002055, 9.370381839011749, 9.367599469107134, 9.404403549896244, 9.313671390709159, 9.100864054418974, 9.110546037131934, 9.210093582192934, 9.35836108112988, 9.45138850434573, 9.442567965833671, 9.354475865470308, 9.298998731060239, 9.677689261206405, 9.73666066634891, 9.493097934565608, 9.534197089424595, 9.346411013323426, 9.304491811937554, 9.304689706262018, 9.82628938521266, 9.837177078403062, 9.619563369400984, 9.612776215591444, 9.567551802948923, 9.503981718238796, 9.327066636406483, 9.162512986732958, 9.298863503523414, 9.339772342285048, 9.310869339019751, 9.282381905667954, 9.27112955641398, 9.191456772556794, 9.36466157211433, 9.391304112246086, 9.479594581448946, 9.354014401682043, 9.381078441906373, 9.28571788232423, 9.368363016265688, 10.384066223311336, 9.957200363513483, 9.691385383720165, 9.637666773800749]
L2=[9.612776215591444, 9.567551802948923, 9.503981718238796, 9.327066636406483, 9.162512986732958, 9.298863503523414, 9.339772342285048, 9.310869339019751, 9.282381905667954, 9.27112955641398, 9.191456772556794, 9.36466157211433, 9.391304112246086, 9.479594581448946, 9.354014401682043, 9.381078441906373, 9.28571788232423, 9.368363016265688, 10.384066223311336, 9.957200363513483, 9.691385383720165, 9.637666773800749, 9.518115965996097, 9.38628875329306, 9.514674140699821, 9.479157968014254, 9.296718254263522, 9.252901060604636, 9.239211494383612, 9.254831468925904, 9.263266586909452, 9.40621384688078, 9.296399283644114, 9.281676239322303, 9.480096140462535, 9.546123919536171, 9.627684938065874, 9.59970395462051, 9.252436278620722, 9.236400403346886, 9.402785521028953, 9.12807453493866, 9.169067907991163, 9.196331538950247, 9.226441082747977, 9.365012699331803, 9.487136244560258, 9.536745916288531, 9.158405363221613, 9.260345158400682]
LS=[L,L2]
"""liste=[]
l=[]
indMaxList=[]
indMaxList.append(NewListe[i].index(max(NewListe[i])))  # liste des indices des maximums avec la fonction "max"
maxList.append(max(NewListe[i]))  # liste des maximums
for j in range(0, len(liste) - 1):
    if j % 28 == 0 and j is not 0:
        l.append(j)  # liste des multiples de 28
        indPic2 = [x + y for x, y in zip(indMaxList,l)]  # liste des multiples de 28 et des indices des maximums pour éviter les répétitions
"""

def maxi(t):

    pic=[]
    p=[]
    # m = t.index(t[-1])
    m = len(t)
    for n in range(1, 11):
        return [j for j,x in enumerate (t[len(t)-38:len(t)-11]) if t[j]-t[j+n]>0 and t[j]-t[j-n]>0 ]
        """for j in range(n - 38+m, n - 11+m):



            #if t[j]-t[j - n] > 0 and t[j] -t[j + n]>0 :  # and (t[j]-2)>>t[j-11] :
                if t[j]-t[j+1]>0 and t[j]-t[j-1]>0:

                    # print("on a un maximum en %d" %j)
                    pic.append(j)
                    p.append(t[j])
                    for i, val in enumerate(pic):
                        if pic.count(val) > 1:
                            pic.remove(val)"""



"""t=maxi(L)
print (t)
t2=maxi(L2)
print (t2)"""
ts=[]
L3=[28,56]
u=[]
for i in range (0,len(LS)):
    ts.append(maxi(LS[i]))
    for j in range(0,len(ts[i])):
        u.append(L3[i])

print ("u",u)
print ("ts",ts)


def add (liste, grandeListe):
    l=[]
    m=[]

    for i in range(0,len(grandeListe)):
        #print(grandeListe[i])
        for j,elt in enumerate(grandeListe[i]):
            #print (elt)
            #m.append(elt+liste[i])
            l.append(elt+liste[i])
    #print(l)
    return l

t=add(L3,ts)
print(t)
L4=[9,9,9]



def somme(UneListe,taille):
    compteur = 0
    accumulateur = 0
    while compteur < taille:
        accumulateur += UneListe[compteur]
        compteur += 1
    return accumulateur


"""def moyenne(UneListe,taille):
    return somme(UneListe,taille) / len(UneListe)

m=moyenne(L,len(L))
print(m)

dist =  6378* acos(sin((48.520641*pi)/180) * sin((48.521874*pi)/180) + cos((48.520641*pi)/180) * cos((48.521874*pi)/180) * cos(
    (7.741601 * pi) / 180-(7.741144*pi)/180))

print (dist)
a=[]
b=6/3
print(len(a))
print(b)

LZ = [[4,2,6,4],[4,2,6,4],[4,2,6,4]]
b =[]
def maFonction(L):
    for elt in L:
        for i in range(len(elt)-1):
            if elt[i]-elt[i+1] >=2:
                b.append(elt[i+1])
    return b


print(maFonction(LZ))

m=[1,2,3,5,8]
for i,n in enumerate(m):
    if n==3:
        m=m[i:i+len(m)]

print("m",m)"""
"""
y=[[1,2,3,5],[1,2,4]]
x=[1,2]
p=[]
g=[9,4]

for i, elt1 in enumerate(x):
    j = 0
    acc = 0
    while j < len(y[i]):
        acc += (y[i][j] - x[i]) ** 2
        j += 1
    moy=acc/len(y[i])
    p.append(moy)
print (p)
print (sqrt(25))"""

x =[[1, 3, 4, 6],[2, 3, 5, 1]]
y = [[2, 3, 5, 1],[1, 3, 4, 6]]
h=[]
a=[]
b=[]
g=[]
t=[]
for i,elt in enumerate(x):
    a.append((y[i][-1] - y[i][0]) / (x[i][-1] - x[i][0]))
    b.append(y[i][0] - a[i] * x[i][0])
    for j in range(0,len(elt)):
        g.append(elt[j])
        if j==x[i][0]:
            h.append(a[i]*x[i][j:j+len(x[i])] +b[i])



print (x)
print("a",a)
print("b",b)
print("g",g)
print (h)
plot(g,h)
show()

