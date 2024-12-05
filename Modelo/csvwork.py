import pandas as pd
import numpy as np
import re


def nivelar_pesos(ruta, n):
    df = pd.read_csv(ruta)
    df_nivelado = df.groupby('Organismo').sample(n = n, random_state=42, )
    df_nivelado.to_csv('Alldatanivel.csv', index=False)

#nivelar_pesos('AlldataRaw.csv',8000)

one_hot_dict = {
    'Humanos' : [1, 0, 0],
    'Bacteria' : [0, 1, 0],
    'Virus' : [0, 0, 1]
}
def etiquetar_organismos(ruta):
    df = pd.read_csv(ruta)
    df['Organismo_vector'] = df['Organismo'].apply(lambda x: one_hot_dict[x])
    df.to_csv('Alldatanivelfinal.csv')

#etiquetar_organismos('Alldatanivel.csv')

#df = pd.read_csv('Alldatanivelfinal.csv')
#print(df.head())

#columna = df['Sequencias']
def convertir_a_array(cadena):
    # Remover caracteres no deseados
    cadena_limpia = re.sub(r'[\[\]]', '', cadena)  # Quita los corchetes
    # Convertir la cadena limpia a una lista de listas
    filas = [list(map(int, fila.split())) for fila in cadena_limpia.split('\n')]
    # Convertir a array de NumPy
    return np.array(filas)

#sequences = df['Sequencias'].apply(convertir_a_array)
# Aplicar la función a la columna


#sequences_lengths = sequences.apply(lambda x: x.shape[0])  # Obtener longitudes de las secuencias
#print(sequences_lengths.value_counts())  # Verificar si todas tienen la misma longitud

# Ejemplo: accediendo al primer array
#primer_array = arrays.iloc[0]
#print(primer_array)



