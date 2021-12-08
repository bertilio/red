import pickle


NONE = '.'

parametro_r = [0.7]
parametro_v = [0.5]
parametro_E = [0.8]
iteracion = [0]




class agente:

    def __init__(self,color):
        self.estados = []
        self.color = color

    def guardar(self,archivo): 

        archivo = open(archivo+'.pickle','wb')
        array = [self.iteracion,self.estados]
        sys.setrecursionlimit(100000)
        pickle.dump(array,archivo)
        archivo.close()

    def cargar(self,archivo):

        archivo = open(archivo+'.pickle','rb')
        array = pickle.load(archivo)
        self.iteracion = array[0] 
        self.estados = array[1] 

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
    








   





