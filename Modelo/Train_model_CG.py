import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models, Input, Model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
import pandas as pd
import re
import json

if __name__ == "__main__":
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
    porcentage = df['porcentage_CG']

    # Convertir a un array 3D (n_samples, 200, 4) o (n_samples, 1)
    X_seq = np.stack(sequences.to_numpy())  # Convertir la serie de arrays a un array 3D
    X_por = np.array(porcentage.to_numpy()).reshape(-1, 1)

    # Procesar `y` (Organismo_vector)
    df['Organismo_vector'] = df['Organismo_vector'].apply(json.loads)  # Asegurarse de que sea un NumPy array
    y = np.array(df['Organismo_vector'].tolist(), dtype="int32")

    # Crear inputs
    input_seq = Input(shape=(200, 4), name='input_seq')  # Input para hot encoding
    input_cg = Input(shape=(1,), name='input_cg')        # Input para %CG

    # Flujo para las secuencias con mejoras
    x = layers.Conv1D(filters=32, kernel_size=10, activation='relu', kernel_regularizer=l2(0.01))(input_seq)
    x = layers.BatchNormalization()(x)  # Normalización para estabilizar el aprendizaje
    x = layers.MaxPooling1D(pool_size=2)(x)
    x = layers.Dropout(0.3)(x)  # Dropout para regularizar

    x = layers.Conv1D(filters=64, kernel_size=5, activation='relu', kernel_regularizer=l2(0.01))(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(pool_size=2)(x)
    x = layers.Dropout(0.3)(x)

    x = layers.Flatten()(x)

    # Combinar los inputs
    combined = layers.concatenate([x, input_cg])

    # Capas densas con mejoras
    z = layers.Dense(128, activation='relu', kernel_regularizer=l2(0.01))(combined)
    z = layers.Dropout(0.4)(z)  # Dropout para prevenir sobreajuste
    output = layers.Dense(3, activation='softmax')(z)

    # Crear el modelo funcional
    modelo = Model(inputs=[input_seq, input_cg], outputs=output)

    # Usar un optimizador con tasa de aprendizaje baja
    opt = tf.keras.optimizers.Adam(learning_rate=0.0001)

    # Compilar el modelo
    modelo.compile(optimizer=opt,
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])

    # Early Stopping para detener el entrenamiento si no mejora
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Entrenar el modelo
    history = modelo.fit([X_seq, X_por], y,
                         batch_size=32,
                         epochs=50,  # Incrementar épocas ya que EarlyStopping detendrá automáticamente
                         verbose=1,
                         validation_split=0.2,
                         callbacks=[early_stopping])

    # Guardar el modelo
    modelo.save("mi_modelo_con_CG_mejorado.h5")
    modelo.save('my_model_con_CG_mejorado.keras')
    with open('history.json', 'w') as f:
        json.dump(history.history, f)
