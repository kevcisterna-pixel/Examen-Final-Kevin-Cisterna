import os
import time
from flask import Flask
import psycopg2

app = Flask(__name__)

# Obtener credenciales desde variables de entorno
DB_HOST = os.environ.get("DB_HOST", "db_container")
DB_NAME = os.environ.get("DB_NAME", "vzeta_db")
DB_USER = os.environ.get("DB_USER", "vzeta_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "vzeta_password")

def get_db_connection():
    # Reintentar conexión si la base de datos tarda en iniciar
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)
    raise Exception("No se pudo conectar a PostgreSQL")

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Crear tabla de visitas si no existe
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visitas (
            id SERIAL PRIMARY KEY,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Registrar la visita actual
    cur.execute('INSERT INTO visitas DEFAULT VALUES;')
    conn.commit()
    
    # Contar el total de visitas registradas
    cur.execute('SELECT COUNT(*) FROM visitas;')
    total_visitas = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return f"<h1>¡Bienvenido a VZeta App!</h1><p>Esta página ha sido visitada <b>{total_visitas}</b> veces.</p>"

if __name__ == '__main__':
    init_db()
    # Escucha en el puerto 5000 dentro del contenedor
    app.run(host='0.0.0.0', port=5000)
