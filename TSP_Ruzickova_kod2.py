#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import random
from math import inf


# In[2]:


uzly = np.loadtxt('benesov_sourad.csv', skiprows = 1, delimiter = ';')
uzly2 = np.loadtxt('orp_sourad.csv', skiprows = 1, delimiter = ';')

plt.plot(uzly[:, 0], uzly[:, 1], 'go')
plt.axis('equal')
plt.ticklabel_format(axis = 'y', style = 'plain')

plt.figure()
plt.plot(uzly2[:, 0], uzly2[:, 1], 'go')
plt.axis('equal')
plt.ticklabel_format(axis = 'y', style = 'plain')


# In[3]:


#print(uzly)


# In[4]:


# NEAREST NEIGHBOUR
def NN(uzly):
    predchudci = []
    delky = []

    # postupne bere vsechny uzly ze seznamu jako pocatecni
    for pu in range(len(uzly)):  
        # zalozi seznam predchudcu P
        P = [-1] * len(uzly)  
        # zalozi seznam stavu S, vsechny uzly jsou zpocatku otevrene
        S = ['O'] * len(uzly)  

        # se zkoumanym uzlem u pracuje jako s pocatecnim
        u = pu
        # zkoumany uzel nastavi jako uzavreny
        S[u] = 'C'
        # delku kruznice grafu inicializuje jako 0
        delkaKruznice = 0

        # postupně priradi ke kruznici vsechny uzly ze seznamu (krome pocatecniho)
        for i in range(len(uzly)-1):
            # provizorni delku kruznice dk inicializuje jako nekonecne dlouhou
            dk = inf

            # pro kazdy uzel:
            for v0 in range(len(uzly)):   
                # pokud je tento uzel otevreny a zaroven dk je vetsi nez vzdalenost mezi zkoumanym uzlem a jeho sousedem:
                if ((S[v0] == 'O') & (dk > np.linalg.norm(uzly[u] - uzly[v0]))):  
                    # dk nastavi jako vzdalenost mezi temito dvema uzly
                    dk = np.linalg.norm(uzly[u] - uzly[v0]) 
                    # do v si ulozim nejblizsiho souseda zkoumaneho uzlu u
                    v = v0

            # uzel v nastavi jako uzaverny
            S[v] = 'C'  
            # predchudce uzlu v je uzel u
            P[v] = u
            # s uzlem v dale pracuje jako s u
            u = v
            # k delce kruznice pricte prave nalezenou vzdalenost
            delkaKruznice = delkaKruznice + dk

        # propojeni cesty v kruznici
        P[pu] = v
        # do seznamu delky prida v kazdem cyklu delku kruznice
        delky.append(delkaKruznice + np.linalg.norm(uzly[pu] - uzly[v]))  
        # do seznamu predchudi prida v kazdem cyklu seznam predchudcu (P) pro danou nalezenou kruznici
        predchudci.append(P)
        
    dk = inf

    # pro kazdou delku v seznamu delek:
    for i in range(len(delky)):
         # hleda i-tou pozici, na ktere je nejkratsi hodnota delky
        if (dk > delky[i]):
            dk = delky[i]
            min_kruznice = i
    
    # Do promene delka ulozi delku pomoci pozice v seznamu delek, kde je nejnizsi hodnota
    delka = delky[min_kruznice]
    
    plt.plot(uzly[:, 0], uzly[:, 1], 'go')
    plt.axis('equal')
    plt.title(round(delka))
    plt.ticklabel_format(axis = 'y', style = 'plain')

    # vykresleni grafu
    for u in range(len(predchudci)):
        plt.plot([uzly[u, 0], uzly[predchudci[min_kruznice][u], 0]], [uzly[u, 1], uzly[predchudci[min_kruznice][u], 1]], 'b-')
    
    return predchudci, delky


# In[5]:


# BEST INSERTION
def BI(uzly):
    # zalozi vychozi kruznici ze tri prvnich bodu seznamu
    kruznice = [0, 1, 2, 0]
    # spocita delku vychozi kruznice
    delka_bi = np.linalg.norm(uzly[kruznice[0]] - uzly[kruznice[1]]) + np.linalg.norm(uzly[kruznice[1]] - uzly[kruznice[2]]) + np.linalg.norm(uzly[kruznice[2]] - uzly[kruznice[3]])
    # vsechny uzly nastavi jako otevrene
    S = ['O'] * len(uzly)
    # prvni tri uzly (tvorici vychozi kruznici) nastavi jako uzavrene
    S[0] = S[1] = S[2] = 'C'
    # zalozeni fronty
    Q = [1] * (len(uzly) - 3)

    plt.figure()
    plt.plot(uzly[:, 0], uzly[:, 1], 'go')
    plt.axis('equal')
    plt.title(round(delka_bi))
    plt.ticklabel_format(axis = 'y', style = 'plain')

    # vykresleni vychozi kruznice
    for u in range(len(kruznice) - 1):
        plt.plot([uzly[kruznice[u], 0], uzly[kruznice[u + 1], 0]], [uzly[kruznice[u], 1], uzly[kruznice[u + 1], 1]], 'b-')

    # dokud fronta neni prazdna:    
    while Q:
        # provizorni delku kruznice dk_bi nastavi jako nekonecne dlouhou
        dk_bi = inf
        # generuje nahodne cislo - nahodnou pozici v seznamu uzlu
        randn = random.randrange(0, len(uzly))

        # pokud uzel na vygenerovane pozici je otevreny, uzavre ho, a spusti se nasledujici for cyklus
        if (S[randn] == 'O'):
            S[randn] = 'C'

            # tolikrat, kolik hran (stran) ma kruznice:
            for i in range(len(kruznice) - 1):
                # hledani optimalni hrany pro pripojeni uzlu
                    if (dk_bi > delka_bi - np.linalg.norm(uzly[kruznice[i]] - uzly[kruznice[i + 1]]) + np.linalg.norm(uzly[kruznice[i]] - uzly[randn]) + np.linalg.norm(uzly[randn] - uzly[kruznice[i + 1]])):
                        dk_bi = delka_bi - np.linalg.norm(uzly[kruznice[i]] - uzly[kruznice[i + 1]]) + np.linalg.norm(uzly[kruznice[i]] - uzly[randn]) + np.linalg.norm(uzly[randn] - uzly[kruznice[i + 1]])
                        # pozici i si zapamatuje jako promennou v
                        v = i

            # do seznamu kruznice priradi zkoumany bod na optimalni pozici
            kruznice.insert(v + 1, randn)
            # delka kruznice se prepise jako dk_bi
            delka_bi = dk_bi
            # z fronty se odebere jeden prvek
            Q.pop(0)
    
    plt.figure()
    plt.plot(uzly[:, 0], uzly[:, 1], 'go')
    plt.axis('equal')
    plt.title(round(delka_bi))
    plt.ticklabel_format(axis = 'y', style = 'plain')

    # vykresleni grafu pomoci cyklu, kdy se vzdy vykresli hrana spojujici bod a jeho predchudce
    for u in range(len(kruznice) - 1):
        plt.plot([uzly[kruznice[u], 0], uzly[kruznice[u + 1], 0]], [uzly[kruznice[u], 1], uzly[kruznice[u + 1], 1]], 'b-')
    
    return kruznice, delka_bi


# In[6]:


P, D = NN(uzly)
k, d = BI(uzly)


# In[7]:


kNN, dNN = NN(uzly2)
kBI, dBI = BI(uzly2)


# In[ ]:




