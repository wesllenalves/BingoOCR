from flask import Flask, jsonify, request, json
from easyocr import Reader
from PIL import Image
import re
import os
import uuid

UPLOAD_FOLDER = 'UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# construit as funcionalidades

@app.route('/')
def homepage():
    return 'A API está no ar'


def recognize(foto):
    lista_idiomas = 'en,pt'
    idiomas = lista_idiomas.split(',')

    gpu = True
    reader = Reader(idiomas, gpu)
    resultados = reader.readtext(foto)

    padrao_data = '^1*([1-9]|[1-8][0-9]|9[0-9]|100)$'

    meuTexto = []
    for (caixa, texto, probabilidade) in resultados:
        if texto.isdigit():
            if re.match(padrao_data, texto):
                meuTexto.append(texto)
    return meuTexto


@app.route('/photo-recognite', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        img = Image.open(file)
        result = recognize(img)

        return json.dumps({'Numeros': result})


# rodar a nossa api
app.run()
