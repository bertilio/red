 
from juego import partida2, Game , partida3 , partida4 , partidaVer
from itertools import groupby, chain
from agente import agente
from red import red
import math
import random
import time
import os

a = agente('R');
a2 = agente('Y');

def iniciar2agentes():
    a.color='R'
    a2.color ='Y'


def cargar():
    a.cargar("agente1")
    a2.cargar("agente2")    


        



iniciar2agentes()

cargar()



#RED NEURONAL APROXIMAR QS

red = red(1,a)

red.introducir()


red.entrenar(1000000)

red.guardar()

#red.cargar()
"""
partida = 0

for i in range(len(a.estados)):

    if partida == 10:
        a.estados[i].imprimir()

    if (a.estados[i].q == -1) or (a.estados[i].q == 1):
        partida = partida +1
       




for e in a.estados:
    e.imprimir()
"""
#estado.imprimir()





#partidavsIA()

#ver(red)