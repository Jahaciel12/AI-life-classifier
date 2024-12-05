import tensorflow as tf
import numpy as np
from Dataclean import subseqid_a_matrix, subseq_de_200, data_import, porc_CG

def cargar_modelo(ruta_modelo):
    modelo = tf.keras.models.load_model(ruta_modelo)
    return modelo

def cargar_datos(ruta_datos):
    #data preparation cadena
    cadena, id = data_import(ruta_datos)
    lista_sub = subseq_de_200(cadena, id)
    data_inp = subseqid_a_matrix(lista_sub)
    data_inp = np.expand_dims(data_inp, axis=0)

    #CG
    CG_percentage = porc_CG(lista_sub)
    CG_percentage = np.array(CG_percentage)

    return data_inp, CG_percentage

#prediccion y clasficacion
def predict_et_clasi(data_inp, CG, modelo):
    clases_pred = []
    prob_pred = []
    for i in data_inp:
        prediccion = modelo.predict([i, CG])
        print(prediccion)
        for j in prediccion:
            clase = np.argmax(j, axis=0)
            clases_pred.append(clase)
            prob = j[clase]
            prob_pred.append(prob)
            print(f'Clase:{clase}, probabilidad:{100 * prob:.2f}')
    #que clase aparece más
    conteo_clase0 = clases_pred.count(0)
    conteo_clase1 = clases_pred.count(1)
    conteo_clase2 = clases_pred.count(2)

    list_conteo = [conteo_clase0, conteo_clase1, conteo_clase2]
    porcent_conteo = [i/sum(list_conteo) * 100 for i in list_conteo]
    #porcentages de probabildad de fiabilidad cada clase segun modelo
    lisprom_prob0 = [prob_pred[i] for i in range(len(clases_pred)) if clases_pred[i] == 0]
    lisprom_prob1 = [prob_pred[i] for i in range(len(clases_pred)) if clases_pred[i] == 1]
    lisprom_prob2 = [prob_pred[i] for i in range(len(clases_pred)) if clases_pred[i] == 2]

    prom_prob0 = 0
    prom_prob1 = 0
    prom_prob2 = 0
    if len(lisprom_prob0) != 0:
        prom_prob0 = sum(lisprom_prob0)/len(lisprom_prob0)
    if len(lisprom_prob1) != 0:
        prom_prob1 = sum(lisprom_prob1)/len(lisprom_prob1)
    if len(lisprom_prob2) != 0:
        prom_prob2 = sum(lisprom_prob2)/len(lisprom_prob2)


    list_prob = [prom_prob0, prom_prob1, prom_prob2]

    #vemos que clase aparece mas
    maximo = max(list_conteo)
    lista_maximo = [i for i, valor in enumerate(list_conteo) if valor == maximo]


    dict_clasi = {0: 'Humano',
                  1: 'Bacteria',
                  2: 'Virus'}
    # si hay una sola clase dominante, devolvemos esa clase, si no, comparamos las comparamos dependiendo de la fiabilidad
    if len(lista_maximo) == 1:
        return(f'El ADN introducido pertenece a {dict_clasi[lista_maximo[0]]}, porcentage cadena: {porcent_conteo[lista_maximo[0]]}%,'
              f'fiabilidad: {list_prob[lista_maximo[0]] * 100:.2f}%')
    else:
        valor = list_prob.index(max(list_prob))
        return(f'El ADN introducido pertenece a {dict_clasi[valor]}, porcentage cadena: {porcent_conteo[lista_maximo[valor]]}%,'
              f'fiabilidad: {list_prob[valor] * 100:.2f}%')


if __name__ == "__main__":
    modelo = cargar_modelo('my_model_con_CG_mejorado.keras')
    X, X1 = cargar_datos('inputfasta.fasta')
    print(predict_et_clasi(X, X1, modelo))


