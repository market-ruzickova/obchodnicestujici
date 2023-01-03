import numpy as np
import matplotlib.pyplot as plt
import random
from math import inf



uzly = np.loadtxt('benesov_sourad.csv', skiprows = 1, delimiter = ';')
uzly2 = np.loadtxt('orp_sourad.csv', skiprows = 1, delimiter = ';')

plt.plot(uzly[:, 0], uzly[:, 1], 'go')
plt.axis('equal')

plt.figure()
plt.plot(uzly2[:, 0], uzly2[:, 1], 'go')
plt.axis('equal');




#print(uzly)


# NEAREST NEIGHBOUR
def NN(uzly):
    predchudci = []
    delky = []

    # postupne bere vsechny uzly ze seznamu jako pocatecni
    for pu in range(len(uzly)):  
        # zalozi seznam predchudcu
        P = [-1] * len(uzly)  
        # zalozi seznam stavu, vsechny uzly jsou zpocatku otevrene
        S = ['O'] * len(uzly)  

        # se zkoumanym uzlem u pracuje jako s pocatecnim
        u = pu
        # zkoumany uzel nastavi jako uzavreny
        S[u] = 'C'
        # delku kruznice grafu inicializuje jako 0
        delkaKruznice = 0

        # postupně priradime ke kruznici vsechny uzly ze seznamu (krome jednoho - pocatecniho)
        for i in range(len(uzly)-1):
            # provizorni delku kruznice dk inicializuje jako nekonecne dlouhou
            dk = inf

            # pro kazdy uzel:
            for v0 in range(len(uzly)):   
                # pokud je tento uzel otevreny a zaroven provizorni delka kruznice je vetsi nez vzdalenost mezi zkoumanym uzlem a jeho sousedem:
                if ((S[v0] == 'O') & (dk > np.linalg.norm(uzly[u] - uzly[v0]))):  
                    # provizorni delku kruznice nastavim jako vzdalenost mezi temito dvema uzly
                    # zkoumaji se postupne vsichni sousedi, tj najde se ten, ktery je nejblize zkoumanemu uzlu
                    dk = np.linalg.norm(uzly[u] - uzly[v0]) 
                    # do v si ulozim nejblizsiho souseda zkoumaneho uzlu u
                    v = v0

            # uzel v uzavru
            S[v] = 'C'  
            # predchudce uzlu v je uzel u
            P[v] = u
            # s uzlem v pracuji jako s u, tj. dale hledam jeho sousedy
            u = v
            # k delce kruznice prictu vzdalenost, kterou jsem prave nasla
            delkaKruznice = delkaKruznice + dk

        # predchudce pocatecniho uzlu je posledni prirazeny uzel v - propojim cestu v kruznici
        P[pu] = v
        # do seznamu delky pridam v kazdem cyklu delku kruznice, coz je delka nalezene cesty plus vzdalenost mezi prvnim a poslednim uzlem
        delky.append(delkaKruznice + np.linalg.norm(uzly[pu] - uzly[v]))  
        # do seznamu predchudi pridam v kazdem cyklu seznam predchudcu (P) pro danou nalezenou kruznici
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
    plt.title(delka)

    # vykresleni grafu pomoci cyklu, kdy se vzdy vykresli hrana spojující bod u a jeho predchudce
    for u in range(len(predchudci)):
        plt.plot([uzly[u, 0], uzly[predchudci[min_kruznice][u], 0]], [uzly[u, 1], uzly[predchudci[min_kruznice][u], 1]], 'b-')
    
    return predchudci, delky




# BEST INSERTION
def BI(uzly):
    # zalozi vychozi kruznici ze tri prvnich bodu seznamu
    kruznice = [0, 1, 2, 0]
    # spocita delku teto vychozi kruznice
    delka_bi = np.linalg.norm(uzly[kruznice[0]] - uzly[kruznice[1]]) + np.linalg.norm(uzly[kruznice[1]] - uzly[kruznice[2]]) + np.linalg.norm(uzly[kruznice[2]] - uzly[kruznice[3]])
    # vsechny uzly nastavi jako otevrene
    S = ['O'] * len(uzly)
    # první tri uzly (tvorici vychozi kruznici) nastavi jako uzavrene
    S[0] = S[1] = S[2] = 'C'
    # zalozi frontu, kde je tolik prvku, kolik je uzlů, minus tri (vychozi kruznice)
    Q = [1] * (len(uzly) - 3)

    plt.figure()
    plt.plot(uzly[:, 0], uzly[:, 1], 'go')
    plt.axis('equal')
    plt.title(delka_bi)

    # vykresleni vychozi kruznici
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
                # postupne zkousi pocitat delky kruznic, kdyz je nahodny bod pridan pokazde na jinou hranu stavajici hruznice
                # pokud je tato vzdalenost kratsi nez dk_bi, dk_bi se prepise na tuto delku
                # timto zpusobem se najde, na jakou pozici ve stavajici kruznici se ma zkoumany nahodny bod pridat
                if (dk_bi > delka_bi - np.linalg.norm(uzly[kruznice[i]] - uzly[kruznice[i + 1]]) + np.linalg.norm(uzly[kruznice[i]] - uzly[randn]) + np.linalg.norm(uzly[randn] - uzly[kruznice[i + 1]])):
                    dk_bi = delka_bi - np.linalg.norm(uzly[kruznice[i]] - uzly[kruznice[i + 1]]) + np.linalg.norm(uzly[kruznice[i]] - uzly[randn]) + np.linalg.norm(uzly[randn] - uzly[kruznice[i + 1]])
                    # pozici i si zapamatuje jako promennou v
                    v = i

            # do seznamu kruznice priradi zkoumany bod na nalezenou pozici
            kruznice.insert(v + 1, randn)
            # delka kruznice se prepise jako delka provizorni kruznice (po prvnim cyklu se 4 body)
            delka_bi = dk_bi
            # z fronty se odebere jeden prvek
            Q.pop(0)
    
    plt.figure()
    plt.plot(uzly[:, 0], uzly[:, 1], 'go')
    plt.axis('equal')
    plt.title(delka_bi)

    # vykresleni grafu pomoci cyklu, kdy se vzdy vykresli hrana spojujici bod a jeho predchudce
    for u in range(len(kruznice) - 1):
        plt.plot([uzly[kruznice[u], 0], uzly[kruznice[u + 1], 0]], [uzly[kruznice[u], 1], uzly[kruznice[u + 1], 1]], 'b-')
    
    return kruznice, delka_bi




P, D = NN(uzly)
k, d = BI(uzly)


kNN, dNN = NN(uzly2)
kBI, dBI = BI(uzly2)






