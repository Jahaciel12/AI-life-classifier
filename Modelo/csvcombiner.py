import pandas as pd


#para convinar diferentes csvs en 1 solo

archivos_csv = ['Corona.csv', 'Ecoli.csv', 'Agro.csv', 'Humano.csv', 'VIH.csv', 'Herpes1.csv', 'Mimivirus.csv']
dataframes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    dataframes.append(df)

df_cominado = pd.concat(dataframes, ignore_index=True)

df_cominado.to_csv('AlldataRaw.csv')