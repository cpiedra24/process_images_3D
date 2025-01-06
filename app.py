from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from PIL import Image
import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde tu frontend

# Inicializar Firebase
cred = credentials.Certificate("firebase/firebase_key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-app.appspot.com'
})
bucket = storage.bucket()

# Ruta para cargar una imagen y procesarla
@app.route('/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    image_path = os.path.join('uploads', file.filename)
    file.save(image_path)

    # Procesar la imagen (por ahora solo un placeholder)
    model_path = os.path.join('models', 'mascota_model.gltf')
    with open(model_path, 'w') as f:
        f.write('dummy content')  # Reemplaza con la lógica real para generar el modelo

    # Subir a Firebase Storage
    blob = bucket.blob(f'models/{file.filename.split(".")[0]}.gltf')
    blob.upload_from_filename(model_path)
    blob.make_public()

    return jsonify({'modelLink': blob.public_url}), 200

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    app.run(debug=True)
