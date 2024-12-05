import pandas as pd
import numpy as np
df = pd.read_csv('Datos modelo/Alldatanivelfinal.csv')

porcentage = df['porcentage_CG']
X_por = np.array(porcentage.to_numpy()).reshape(-1, 1)

print(X_por)