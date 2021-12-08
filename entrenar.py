 

from agente import agente
from red import red

a = agente('R');

def iniciar2agentes():
    a.color='R'


def cargar():
    a.cargar("agente1")
    print("AGENTE 1 CARGADO")

        



iniciar2agentes()

cargar()



#RED NEURONAL APROXIMAR QS

red = red(1,a)

red.introducir()

del a


red.cargarDatos("red")

red.entrenar(1000000)

red.guardar()
