import matplotlib.pyplot as plt
import json

with open('history.json', 'r') as f:
    history = json.load(f)

# Graficar la pérdida
plt.plot(history['loss'], label='Pérdida de entrenamiento')
plt.plot(history['val_loss'], label='Pérdida de validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()
plt.title('Pérdida durante el entrenamiento')
plt.show()

# Graficar la precisión
plt.plot(history['accuracy'], label='Precisión de entrenamiento')
plt.plot(history['val_accuracy'], label='Precisión de validación')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()
plt.title('Precisión durante el entrenamiento')
plt.show()