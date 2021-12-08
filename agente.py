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
    
    








   





