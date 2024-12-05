import pandas as pd
from Bio import SeqIO
import numpy as np

def data_import(ruta):
    seq = []
    id = []
    with open(ruta, 'r') as handle:
        for sec in SeqIO.parse(handle, "fasta"):
            seq.append(sec.seq)
            id.append(sec.id)
    return seq, id
#separa todas las sequencias en subsequencias de 200 nuc
def subseq_de_200(seq, id):
    lista_seq200 = []
    for cadena, ide in zip(seq, id):
        if len(cadena) >= 200:
            for pack in range(0, len(cadena), 200):
               a = cadena[pack:pack+200]
               if len(a) == 200 and all(i in "ACTG" for i in a):
                    lista_seq200.append([a, ide])
    #Es una lista con listas donde hay las sequencias de 200pb y su id
    return lista_seq200
#vectoriza nuc en una lista
def subseqid_a_matrix(subseqid_para_cambiar):
    matrizes_de_cadenas = []
    sequencias = [sublista[0] for sublista in subseqid_para_cambiar]
    for cadena in sequencias:
        matriz = []
        for nuc in cadena:
            if nuc == 'A':
                matriz.append([1, 0, 0, 0])
            elif nuc == 'C':
                matriz.append([0, 1, 0, 0])
            elif nuc == 'G':
                matriz.append([0, 0, 1, 0])
            elif nuc == 'T':
                matriz.append([0, 0, 0, 1])
            else:
                print('Error en cadena, carácteres no validos')
                break
        matriz_real = np.array(matriz)
        matrizes_de_cadenas.append(matriz_real)
        #lista con una lista con los vectores
    return matrizes_de_cadenas


def porc_CG(lista_de_listas):
    sequencias = [sublista[0] for sublista in lista_de_listas]
    cg_porcent = []
    for sec in sequencias:
        cg_count = 0
        for nuc in sec:
            if nuc == 'C' or nuc == 'G':
                cg_count += 1
        cg_porcent.append(round(cg_count/len(sec) * 100, 2))
    return cg_porcent
#introducir las listas para confromar el csv
def lista_a_csv(idlist, matrizes, organismo, CG_porc, archivos_csv):
    print(f"Longitud de ID seq: {len(idlist)}")
    print(f"Longitud de Sequencias: {len(matrizes)}")
    data = {
        'ID seq' : idlist,
        'Sequencias' : matrizes,
        'porcentage_CG' : CG_porc
    }
    df = pd.DataFrame(data)
    df['Organismo'] = organismo
    df.to_csv(archivos_csv)
    print('Archivo creado correctamente')

archivos_fasta = ['fastaCorona.fasta', 'fastaEcoli.fasta', 'fastagro.fasta', 'fastahumanos.fasta', 'fastaVIH.fasta',
            'Herpes1.fasta', 'Mimivirus.fasta']
archivos_csv = ['Corona.csv', 'Ecoli.csv', 'Agro.csv', 'Humano.csv', 'VIH.csv', 'Herpes1.csv', 'Mimivirus.csv']
organismos_lista = ['Virus', 'Bacteria', 'Bacteria', 'Humanos', 'Virus', 'Virus', 'Virus']
if __name__ == "__main__":
    for datos in range(len(archivos_fasta)):
        ruta = archivos_fasta[datos]
        organismo = organismos_lista[datos]
        seq, id = data_import(ruta)
        subseqid_para_cambiar = subseq_de_200(seq, id)
        matriz_vectores = subseqid_a_matrix(subseqid_para_cambiar)
        porcentage = porc_CG(subseqid_para_cambiar)
        print(matriz_vectores)
        lista_a_csv([sublista[1] for sublista in subseqid_para_cambiar], matriz_vectores, organismo, porcentage, archivos_csv[datos])

