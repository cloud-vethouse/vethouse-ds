import pandas as pd
from sqlalchemy import create_engine
import boto3
import os

# Configuración basada en tus datos de MS2
DB_USER = 'postgres'
DB_PASS = '1234'
DB_HOST = '172.31.47.67'
DB_PORT = '5436' 
DB_NAME = 'veterinaria_db'
S3_BUCKET = 'vethouse-data-science'

def extraer_y_cargar():
    try:
        # Cadena de conexión PostgreSQL
        conn_str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(conn_str)
        
        # Tablas identificadas por los endpoints de la UI
        tablas = ['citas', 'mascotas', 'veterinarios'] 
        
        s3 = boto3.client('s3')
        
        for tabla in tablas:
            print(f"--- Extrayendo de Postgres (MS2): {tabla} ---")
            
            # Extraemos los datos para el análisis de DS
            df = pd.read_sql(f"SELECT * FROM {tabla}", engine)
            
            csv_file = f"{tabla}.csv"
            df.to_csv(csv_file, index=False)
            
            # Destino en el Data Lake
            s3_path = f"raw/appointments/{csv_file}"
            s3.upload_file(csv_file, S3_BUCKET, s3_path)
            
            print(f"✅ ÉXITO: s3://{S3_BUCKET}/{s3_path}")
            
            if os.path.exists(csv_file):
                os.remove(csv_file)
                
    except Exception as e:
        print(f"❌ ERROR EN INGESTA APPOINTMENTS: {e}")

if __name__ == "__main__":
    extraer_y_cargar()
