import pandas as pd
from pymongo import MongoClient
import boto3
import os

# Configuración basada en el docker-compose de tus compañeros
MONGO_URI = "mongodb://root:password@172.31.47.67:27017/"
DB_NAME = "mongo-treatments" # PROBAR NOMBRE
COLLECTION_NAME = "consultas" 
S3_BUCKET = 'vethouse-data-science'

def ingesta_mongo():
    try:
        # 1. Conexión a MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        col = db[COLLECTION_NAME]
        
        print(f"--- Extrayendo documentos de MongoDB: {COLLECTION_NAME} ---")
        
        # 2. Obtener datos
        datos = list(col.find())
        
        if not datos:
            print("⚠️ No se encontraron documentos. Verificando si hay datos en la DB...")
            return

        # 3. Procesar datos (Aplanamos el JSON de Mongo)
        df = pd.DataFrame(datos)
        if '_id' in df.columns:
            df = df.drop(columns=['_id'])

        # 4. Guardar y Subir a S3
        csv_file = "consultas_tratamientos.csv"
        df.to_csv(csv_file, index=False)
        
        s3 = boto3.client('s3')
        s3_path = f"raw/treatments/{csv_file}"
        s3.upload_file(csv_file, S3_BUCKET, s3_path)
        
        print(f"✅ ÉXITO: s3://{S3_BUCKET}/{s3_path} subido correctamente.")
        
        if os.path.exists(csv_file):
            os.remove(csv_file)

    except Exception as e:
        print(f"❌ ERROR EN INGESTA TREATMENTS: {e}")

if __name__ == "__main__":
    ingesta_mongo()
