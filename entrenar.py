 

from agente import agente
from red import red

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
