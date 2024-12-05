import tensorflow as tf
import numpy as np
from Dataclean import subseqid_a_matrix, subseq_de_200, data_import

# Cargar el modelo desde el archivo
modelo = tf.keras.models.load_model("my_model.keras")

#data preparation
cadena, id = data_import('inputfasta.fasta')
lista_sub = subseq_de_200(cadena, id)
data_inp = subseqid_a_matrix(lista_sub)
data_inp = np.expand_dims(data_inp, axis=0)  # Nueva forma será (1, n_muestras, 200, 4)#no entiendo lo del1,poresobucle
print(data_inp)
for j in data_inp:
    print(j.shape)

#prediccion y clasficacion
clases_pred = []
prob_pred = []
for i in data_inp:
    prediccion = modelo.predict(i)
    print(prediccion)
    for j in prediccion:
        clase = np.argmax(j, axis=0)
        clases_pred.append(clase)
        prob = j[clase]
        prob_pred.append(prob)
        print(f'Clase:{clase}, probabilidad{100 * prob:.2f}')
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
    print(f'El ADN introducido pertenece a {dict_clasi[lista_maximo[0]]}, porcentage cadena: {porcent_conteo[lista_maximo[0]]}%,'
          f'fiabilidad: {list_prob[lista_maximo[0]] * 100}%')
else:
    valor = list_prob.index(max(list_prob))
    print(f'El ADN introducido pertenece a {dict_clasi[valor]}, porcentage cadena: {porcent_conteo[lista_maximo[valor]]}%,'
          f'fiabilidad: {list_prob[valor] * 100}%')





