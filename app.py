from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# Pega tu cadena de conexión de MongoDB Atlas aquí:
MONGO_URI = "mongodb+srv://admin:TU_CONTRASEÑA@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URI)
    db = client['GeoSOS_DB']       # Nombre de tu base de datos
    collection = db['bitacora']    # Nombre de tu colección
    print("✅ Conexión exitosa a MongoDB")
except Exception as e:
    print("❌ Error conectando a Mongo:", e)

@app.route('/')
def home():
    return "Servidor GeoSOS (Python) Activo 🐍"

@app.route('/guardar', methods=['POST'])
def guardar_alerta():
    try:
        data = request.json
        print("📥 Recibido:", data)
        
        # Crear el documento para Mongo
        nuevo_registro = {
            "fecha": datetime.utcnow(),
            "usuario": data.get('usuario', 'Desconocido'),
            "ci": data.get('ci', 'N/A'),
            "tipo": data.get('tipo', 'TEST'),
            "ubicacion": data.get('ubicacion', {}),
            "detalles": data.get('detalles', {})
        }

        # Insertar en la base de datos
        resultado = collection.insert_one(nuevo_registro)
        
        return jsonify({
            "status": "Exito", 
            "id": str(resultado.inserted_id)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)