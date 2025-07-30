from dotenv import load_dotenv
import pandas as pd
import psycopg2
import os

load_dotenv()

def load_to_csv(data, path="./data/processed/Propiedades_FincaRaiz.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    print(f"✅ Guardado exitoso en {path}")


def load_to_postgres(df):
    conn= psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS propiedades (
            id SERIAL PRIMARY KEY,
            precio INTEGER,
            arrendador TEXT,
            habitaciones INTEGER,
            banos INTEGER,
            area INTEGER
        )
    """)
    conn.commit()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO propiedades (precio, arrendador, habitaciones, banos, area)
            VALUES (%s, %s, %s, %s, %s)
        """, 
        (
        row['Precio'],
        row['Arrendador'],
        row['habitaciones'],  # <-- corregido
        row['baños'],         # <-- incluye tilde
        row['area']
        ))
    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Datos cargados en PostgreSQL correctamente.")