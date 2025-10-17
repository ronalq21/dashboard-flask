from flask import Flask, render_template, request, redirect, jsonify
import os, subprocess, sys

app = Flask(__name__)

# Ruta absoluta de la carpeta codigos
RUTA_CODIGOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'codigos')

@app.route('/')
def inicio():
    datos_usuario = {
        'nombre': 'Ronaldhino',
        'apellidos': 'Jinez Incacutipa',
        'carrera': 'Ingenieria Estadística e Informática',
        'universidad': 'Universidad del Altiplano Puno',
        'año_ingreso': 2023,
        'foto': 'img/foto.jpg'
    }
    archivos = [f for f in os.listdir(RUTA_CODIGOS) if f.endswith('.py')]
    return render_template('index.html', usuario=datos_usuario, archivos=archivos)

@app.route('/upload', methods=['POST'])
def upload():
    archivo = request.files['archivo']
    if archivo.filename.endswith('.py'):
        archivo.save(os.path.join(RUTA_CODIGOS, archivo.filename))
    return redirect('/')

@app.route('/run/<nombre>', methods=['POST'])
def run(nombre):
    ruta = os.path.join(RUTA_CODIGOS, nombre)
    try:
        salida = subprocess.check_output([sys.executable, ruta], text=True)
    except subprocess.CalledProcessError as e:
        salida = e.output or str(e)
    return jsonify({"salida": salida})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
