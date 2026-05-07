import pandas as pd
from sqlalchemy import create_engine
import boto3
import os

# Configuración de conexión 3306 debe estar abierto en security
DB_USER = 'admin'
DB_PASS = 'vethouse2024'
DB_HOST = '172.31.47.67'
DB_NAME = 'vethouse_pets'
S3_BUCKET = 'vethouse-data-science'

def extraer_y_cargar():
    try:
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
        s3 = boto3.client('s3')
        
        tablas = ['duenos', 'mascotas']
        
        for tabla in tablas:
            print(f"--- Iniciando extracción de: {tabla} ---")
            
            # 1. Extraer datos
            df = pd.read_sql(f"SELECT * FROM {tabla}", engine)
            
            # 2. Guardar temporalmente
            csv_file = f"{tabla}.csv"
            df.to_csv(csv_file, index=False)
            
            # 3. Subir a S3
            s3_path = f"raw/pets/{csv_file}"
            s3.upload_file(csv_file, S3_BUCKET, s3_path)
            
            print(f"✅ ÉXITO: s3://{S3_BUCKET}/{s3_path} subido correctamente.")
            
            # Limpiar archivo local
            if os.path.exists(csv_file):
                os.remove(csv_file)
                
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    extraer_y_cargar()
