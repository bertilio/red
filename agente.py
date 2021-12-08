
from itertools import groupby, chain
import math
import pickle
import random
import numpy
import sys


NONE = '.'

parametro_r = [0.7]
parametro_v = [0.5]
parametro_E = [0.8]
iteracion = [0]




class agente:

    def __init__(self,color):
        self.estados = []
        self.generacion_max = [0]
        self.parametro_r = parametro_r
        self.parametro_v = parametro_v
        self.parametro_E = parametro_E
        self.iteracion = iteracion
        self.color = color
        self.red = False

    def guardar(self,archivo): 

        archivo = open(archivo+'.pickle','wb')
        array = [self.iteracion,self.estados]
        sys.setrecursionlimit(100000)
        pickle.dump(array,archivo)
        archivo.close()

    def actualizarQs(self):
        self.estados[0].setQ()

    def cargar(self,archivo):

        archivo = open(archivo+'.pickle','rb')
        array = pickle.load(archivo)
        self.iteracion = array[0] 
        self.estados = array[1] 
    
    def existe(self,tablero):
        for estado in self.estados:
            if tablero == estado.tablero:
                return estado
        return False
    
    def existen(self,estados_nuevos): #DEVUELVE UNA LISTA DE ESTADOS FORMADA POR LOS QUE ENTRAN Y NO EXISTEN Y LOS QUE EXISTEN SE SUSTITUYEN POR EL YA CREADO ANTERIORMENTE

        #GUARDAMOS LOS TABLEROS DE LOS NUEVOS ESTADOS
        tableros = []
        esta = []

        for e in estados_nuevos:
            tableros.append(e.tablero)
            esta.append(False)


        
        #MIRAMOS QUE TABLEROS ESTAN EN LOS ESTADOS YA GUARDADOS Y LO REPRESENTAMOS EN UN ARRAY CON TRUE SI ESTA Y FALSE SI NO
        for estado in self.estados:
            if estado.tablero in tableros:
                #LO BUSCAMOS EN LOS ESTADOSNUEVOS
                indice = tableros.index(estado.tablero)
                #LO INTERCAMBIAMOS POR EL ESTADO NUEVO QUE COINCIDE
                estados_nuevos[indice] = estado
                esta[indice]=True
        
        return esta
                
    def actualizar(self, pasos, recompensa):

        lista = []

        g = 0

        
        #GENERAMOS LOS OBJETOS ESTADO PARA CADA PASO DE LA PARTIDA

        for tablero in pasos:

            estado = Estado(tablero, g,self.estados)
            g += 1
            lista.append(estado)

        lista.reverse()

        #VEMOS QUE ESTADOS EXISTEN Y CUALES NO
        booleanos = self.existen(lista)

        #GUARDAMOS LOS ESTADOS QUE NO EXISTEN EN LA LISTA AÑADIR

        añadir = []

        for i in range(len(lista)):
            if i < len(lista) - 1:

                if booleanos[i]==False:


                    lista[i].setPadre(lista[i + 1]) #Añades como padre el anterior y te añades a su lista de hijos


                    añadir.append(lista[i])
                
                    #SI EL SIGUIENTE ESTADO YA EXISTE (QUE EN ESTE CASO ES EL ANTERIOR EN LA LISTA PORQUE ESTA DEL REVES) TENEMOS QUE INDICAR QUE ES HIJO
                    
                    if i > 0 :
                        if booleanos[i-1] == True:
                            lista[i].setHijo(lista[i-1])
                            lista[i-1].setPadre(lista[i])
                            
            else:
                if booleanos[i]==False:
                    añadir.append(lista[i])


        if len(añadir) == 0:
            lista[0].cambiar()

        lista[0].q = recompensa

        añadir.reverse()

        for estado in añadir:
            self.estados.append(estado)

        

        self.estados[0].setQ()



        if self.generacion_max[0] < lista[0].generacion:
            self.generacion_max[0] = lista[0].generacion






    def recompensa(self,ganador ):
        if ganador == self.color:
            return 1
        elif ganador == '.':
            return 0.1
        else:
            return -1

    def politica_trucada(self):

        turn = self.color

        row = input('{}\'s turn: '.format(
                    'Red' if turn == 'R' else 'Yellow'))
        return row

    def politica(self,t):

        lista  = [] #LISTA DE ESTADOS

        acciones = [] #LISTA DE CASILLAS DONDE SE PUEDE COLOCAR
        i = 0
        for columna in t: #AÑADIMOS A ACCIONES EL NUMERO DE COLUMNA DE AQUELLAS QUE TENGAN HUECOS LIBRES
            if columna.count('.') > 0:
                acciones.append(i)
            i+=1
    

        estados_acciones = [] #lista de tableros que generarian las acciones posibles

        for a in acciones: #guardamos los tableros generados
            estados_acciones.append(self.simularInsert(t,a))
        

        #añadimos los estados sin actualizar q

        g = 0

        for tablero in estados_acciones: #guardamos en la lista los estados generados por los tableros

            estado = Estado(tablero, g,self.estados)
            g += 1
            lista.append(estado)

        lista.reverse()

        estado = self.existe(t) #guardamos si existe el estado actual, sino lo generamos en el siguiente if

        if not estado:
            
            estado = Estado(t, g,self.estados)

        #Sacamos los hijos del estado

        hs = estado.getHijos()
            


        iterador = iter(hs)

        hijos = []
 
        for e in lista: #Por cada estado de la lista de acciones
            guardar = True
            for h in hs: #por cada hijo ya existente
                if e.tablero == h.tablero: #Si el hijo coincide con el estado de acciones
                    guardar = False #No se guarda el estado de acciones
            if guardar:
                hijos.append(e)
            else:
                hijos.append(next(iterador)) #Se guarda el hijo ya guardado


        factor = 0.01

        qtotal = 0

        for hijo in hijos:
            qtotal += math.e ** (self.parametro_E[0] * self.iteracion[0]* factor * hijo.q)
        
        probabilidades = []


        t = self.iteracion[0]

        for hijo in hijos:
            p = (math.e ** ( self.parametro_E[0] * self.iteracion[0] * factor * hijo.q )) / (qtotal)
            probabilidades.append(p)


        #Elegimos un hijo al azar

        elegido = random.choices(acciones,weights = probabilidades)

        indice = acciones.index(elegido[0])

        """

        for h in range(len(probabilidades)):
            print(hijos[h].q)
            print(probabilidades[h])
            print("-----------------")
        """
        #print("Q DEL ESTADO ELEGIDO: ",hijos[indice].q)
        

        return elegido[0]
    
    def setRed(self,red):
        self.red=red    
    def politicaRed(self,t):

        lista  = [] #LISTA DE ESTADOS

        acciones = [] #LISTA DE CASILLAS DONDE SE PUEDE COLOCAR
        i = 0
        for columna in t: #AÑADIMOS A ACCIONES EL NUMERO DE COLUMNA DE AQUELLAS QUE TENGAN HUECOS LIBRES
            if columna.count('.') > 0:
                acciones.append(i)
            i+=1
    

        estados_acciones = [] #lista de tableros que generarian las acciones posibles

        for a in acciones: #guardamos los tableros generados
            estados_acciones.append(self.simularInsert(t,a))
        
        qs = []

        for t in estados_acciones:
            q = self.red.predecir(t)
            qs.append(q[0][0])

        indice = 0

        max = qs[indice]

        contador = 0 

        if self.color == 'R':

            for q in qs:
                if q > max:
                    max = q
                    indice = contador
                contador+=1
        else:
            for q in qs:
                if q < max:
                    max = q
                    indice = contador
                contador+=1

        print(qs)
        
        return acciones[indice]




        #Elegimos un hijo al azar

        elegido = random.choices(acciones,weights = probabilidades)

        indice = acciones.index(elegido[0])     

        return elegido[0]   

    def simularInsert(self, tablero , column):

        #copia del tablero

        paso = []
        for col in tablero:
            paso.append(col.copy())


        """Insert the color in the given column."""
        c = paso[column]
        if c[0] != NONE:
            return False

        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = self.color
        
        return paso


class Estado:

    def __init__(self, tablero, g,estados):
        self.padres = []
        self.tablero = tablero
        self.q = 0
        self.generacion = g
        self.estados = estados
        self.hijos = []
        self.cambios = False

    def arbolgenealogico(self):
        res = 0
        res += self.countHijos()
        for h in self.hijos:
            res+=h.arbolgenealogico()
        return res

    def setPadre(self, padre):
        self.padres.append(padre)
        padre.setHijo(self)

    def setHijo(self,hijo):
        self.hijos.append(hijo)
        self.cambiar()

    def cambiar(self):
        self.cambios = True
        for padre in self.padres:
            padre.cambiar()
    
    def imprimir(self):
        print()
        print()
        tablero = self.tablero
        print("Estado:")
        print('  '.join(map(str, range(7))))
        for y in range(6):
            print('  '.join(str(tablero[x][y]) for x in range(7)))
        print()
        print("------------------")
        for padre in self.padres:
            print("Padre:")
            tablero = padre.tablero
            print('  '.join(map(str, range(7))))
            for y in range(6):
                print('  '.join(str(tablero[x][y]) for x in range(7)))
            print()
            print("------------------")
        if self.countHijos() > 0:
            for hijo in self.hijos:
                print("Hijo:")
                tablero = hijo.tablero
                print('  '.join(map(str, range(7))))
                for y in range(6):
                    print('  '.join(str(tablero[x][y]) for x in range(7)))
                print()
                print("------------------")

        print("VALOR DE Q: ",self.q)

    def getHijos(self):
        return self.hijos


    def countHijos(self):

        return len(self.getHijos())

    def setQ(self):

        if self.cambios:
            hijos = self.getHijos()

            if (len(hijos) > 0):

                hijos[0].setQ()

                q_hijos = hijos[0].q
                for hijo in hijos:
                    
                    hijo.setQ()
                    q_h = hijo.q
                    if q_hijos < q_h:
                        q_hijos = q_h

                

                self.q = self.q  * (1-parametro_v[0]) + parametro_v[0] * (q_hijos * parametro_r[0])
            self.cambios=False








   





