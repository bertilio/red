import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import threading
from keras.utils.generic_utils import get_custom_objects
from keras.layers import Activation
from mega import Mega

mega = Mega()
m = mega.login("albertovicentedelegido@gmail.com", "USOCw8KsCIO")

class red:

    def __init__(self,id,a):
        self.id = id
        self.data = []
        self.targets = []
        self.a = a
        self.model = False
        self.array0=[]
        self.array1=[]
        self.array2=[]
        self.array3=[]
        self.q0=[]
        self.q1=[]
        self.q2=[]
        self.q3=[]


    def thread_function(self,indice,array):

        print("inicio hilo: ",indice)

        longitud = len(array)

        inicio = int(indice*(longitud/4))
        
        final = int((indice+1)*(longitud/4))

        for i in range(inicio,final):
            
            

            if indice == 0:

                nuevo = []

                for fila in array[i].tablero:
                    for elemento in fila:
                        if elemento == 'R':
                            nuevo.append(1)
                        elif elemento == 'Y':
                            nuevo.append(-1)
                        else:   
                            nuevo.append(0)

                self.array0.append(nuevo)
                self.q0.append( array[i].q)

            elif indice == 1:

                nuevo = []

                for fila in array[i].tablero:
                    for elemento in fila:
                        if elemento == 'R':
                            nuevo.append(1)
                        elif elemento == 'Y':
                            nuevo.append(-1)
                        else:   
                            nuevo.append(0)

                self.array1.append(nuevo)
                self.q1.append( array[i].q)

            elif indice == 2:

                nuevo = []

                for fila in array[i].tablero:
                    for elemento in fila:
                        if elemento == 'R':
                            nuevo.append(1)
                        elif elemento == 'Y':
                            nuevo.append(-1)
                        else:   
                            nuevo.append(0)

                self.array2.append(nuevo)
                self.q2.append( array[i].q)

            else:

                nuevo = []

                for fila in array[i].tablero:
                    for elemento in fila:
                        if elemento == 'R':
                            nuevo.append(1)
                        elif elemento == 'Y':
                            nuevo.append(-1)
                        else:   
                            nuevo.append(0)

                self.array3.append(nuevo)
                self.q3.append( array[i].q)
    
    def convertir(self,array):

        x = threading.Thread(target=self.thread_function, args=(0,array,))
        x1 = threading.Thread(target=self.thread_function, args=(1,array,))
        x2 = threading.Thread(target=self.thread_function, args=(2,array,))
        x3 = threading.Thread(target=self.thread_function, args=(3,array,))

        x.start()
        x1.start()
        x2.start()
        x3.start()

        x.join()
        x1.join()
        x2.join()
        x3.join()

        return [self.array0 + self.array1 + self.array2 + self.array3],[self.q0 + self.q1 + self.q2 + self.q3]


    def introducir(self):

        total = len(self.a.estados)
        
        indice = 0

        estados = self.a.estados

        inputs = []
        outputs = []

        """

        for e in estados:
            os.system("cls")

            porcentaje = indice*100 // total

            print("Cargando datos: " ,porcentaje)
            indice = indice + 1

            nuevo = []

            for fila in e.tablero:
                for elemento in fila:
                    if elemento == 'R':
                        nuevo.append(1)
                    elif elemento == 'Y':
                        nuevo.append(-1)
                    else:   
                        nuevo.append(0)

            inputs.append(nuevo)
            outputs.append(e.q)
        
        """
        resultado = self.convertir(estados)

        print("Fin conversion")

        inputs = resultado[0]
        outputs = resultado[1]

        self.data = np.array(inputs)
        self.targets = np.array(outputs)

        print(self.targets[0])

    def entrenar(self,epocas):

        def custom_activation(x):
            return x

        get_custom_objects().update({'custom_activation': custom_activation})

        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Dense(64, input_dim=42, activation='sigmoid'))
        self.model.add(keras.layers.Dense(16, activation='sigmoid'))
        self.model.add(keras.layers.Dense(1, activation='custom_activation'))

        self.model.summary()

        self.model.compile(loss='mean_squared_error',
            optimizer='adam',
            metrics=['accuracy'])
        
        x_train = self.data[0]
        y_train = self.targets[0]
        self.model.fit(x_train,y_train,epochs=epocas)


    def guardar(self):
    
        # serializar el modelo a JSON
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        
        # serializar los pesos a HDF5
        self.model.save_weights("model.h5")
        file = m.upload("model.json")
        file = m.upload("model.h5")
        print("Modelo Guardado!")
        ##
    def cargar(self):
        
        def custom_activation(x):
            return x

        get_custom_objects().update()

        # cargar json y crear el modelo
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = tf.keras.models.model_from_json(loaded_model_json,custom_objects = {'custom_activation': custom_activation})
        # cargar pesos al nuevo modelo
        self.model.load_weights("model.h5")
        print("Cargado modelo desde disco.")
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    
    def predecir(self,t):

        

        nuevo = []

        for fila in t:
            for elemento in fila:
                if elemento == 'R':
                    nuevo.append(1)
                elif elemento == 'Y':
                    nuevo.append(-1)
                else:   
                    nuevo.append(0)

        a = []

        a.append(nuevo)  

        entrada = np.array(a)

        q = self.model.predict(entrada)

        return q


