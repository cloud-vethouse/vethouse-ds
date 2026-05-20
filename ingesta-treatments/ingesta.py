import pandas as pd
from pymongo import MongoClient
import boto3
import os

# CONFIGURACIÓN BASADA EN TU URI
MONGO_URI = "mongodb://root:password@172.31.17.204:27017/vethouse_clinica?authSource=admin"
DB_NAME = "vethouse_clinica" 
COLLECTION_NAME = "consultas" 
S3_BUCKET = 'vethouse-data-science'

def ingesta_mongo():
    try:
        # 1. Conexión a MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        col = db[COLLECTION_NAME]
        
        print(f"--- Conectando a Mongo en 172.31.17.204 ---")
        
        # 2. Obtener datos
        datos = list(col.find())
        
        if not datos:
            print(f"⚠️ No hay datos en {DB_NAME}.{COLLECTION_NAME}")
            # Verificamos si la colección se llama distinto
            print(f"Colecciones disponibles: {db.list_collection_names()}")
            return

        # 3. PROCESAMIENTO (Aplanamiento para Athena)
        for d in datos:
            d.pop('_id', None) # El ID de Mongo no sirve en Athena
            if 'tratamientos' in d and isinstance(d['tratamientos'], list):
                # Convertimos la lista de objetos a un string legible
                d['tratamientos'] = " | ".join([f"{t.get('tipo','?')}: {t.get('descripcion','?')}" for t in d['tratamientos']])

        # 4. Crear DataFrame
        df = pd.DataFrame(datos)

        # 5. Guardar y Subir a S3
        csv_file = "consultas_tratamientos.csv"
        # Usamos quoting=1 (QUOTE_ALL) para que los textos con comas no rompan las columnas
        df.to_csv(csv_file, index=False, quoting=1) 
        
        s3 = boto3.client('s3')
        s3_path = f"raw/treatments/{csv_file}"
        s3.upload_file(csv_file, S3_BUCKET, s3_path)
        
        print(f"✅ ÉXITO: s3://{S3_BUCKET}/{s3_path} subido correctamente.")
        
        if os.path.exists(csv_file):
            os.remove(csv_file)

    except Exception as e:
        print(f"❌ ERROR EN INGESTA: {e}")

if __name__ == "__main__":
    ingesta_mongo()
