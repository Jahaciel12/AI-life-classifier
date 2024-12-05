from flask import Flask, render_template, request, redirect, url_for
import os
import sys
sys.path.append(os.path.abspath('../Modelo'))
from Modelo_uso_con_CG import cargar_modelo, cargar_datos, predict_et_clasi
app = Flask(__name__)


# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'fasta'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


# Route for handling file uploads
@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        modelo = cargar_modelo('my_model_con_CG.keras')
        X, X1 = cargar_datos(filepath)
        resultado = predict_et_clasi(X, X1, modelo)
        return render_template('result.html', result=resultado)

    else:
        return 'Invalid file type. Only .fasta files are allowed.', 400


if __name__ == '__main__':
    app.run(debug=True)
