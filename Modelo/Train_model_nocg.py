import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models
import pandas as pd
import re
import json

# Cargar datos
df = pd.read_csv('Datos modelo/Alldatanivelfinal.csv')

# Procesar columna `Sequencias` para convertir a array 3D
def convertir_a_array(cadena):
    # Remover caracteres no deseados
    cadena_limpia = re.sub(r'[\[\]]', '', cadena)  # Quita los corchetes
    # Convertir la cadena limpia a una lista de listas
    filas = [list(map(int, fila.split())) for fila in cadena_limpia.split('\n')]
    # Convertir a array de NumPy
    return np.array(filas)

# Aplicar la función a toda la columna
sequences = df['Sequencias'].apply(convertir_a_array)

# Convertir a un array 3D (n_samples, 200, 4)
X = np.stack(sequences.to_numpy())  # Convertir la serie de arrays a un array 3D

# Procesar `y` (Organismo_vector)
df['Organismo_vector'] = df['Organismo_vector'].apply(json.loads)  # Asegurarse de que sea un NumPy array
y = np.array(df['Organismo_vector'].tolist(), dtype="int32")


modelo = models.Sequential()

modelo.add(layers.Conv1D(filters = 32, kernel_size = 10, activation = 'relu', input_shape = (200,4)))
modelo.add(layers.MaxPooling1D(pool_size = 2))
#Reduce la dimensión del dato. En este caso, toma el valor más alto de
# cada grupo de 2 bases (pool_size=2), reduciendo la longitud a la mitad (200 → 100).
modelo.add(layers.Conv1D(filters = 64, kernel_size = 5, activation= 'relu'))
modelo.add(layers.MaxPooling1D(pool_size = 2))
modelo.add(layers.Flatten()) #para conectar capas convu con densas
modelo.add(layers.Dense(128, activation = 'relu'))
modelo.add(layers.Dense(3, activation = 'softmax'))

modelo.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = modelo.fit(X, y, batch_size = 32, epochs = 15, verbose = 1, validation_split = 0.2)

modelo.save("mi_modelo.h5")
modelo.save('my_model.keras')