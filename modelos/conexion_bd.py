import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env
load_dotenv()


def obtener_conexion():
    """
    Devuelve una conexión activa a la base de datos usando datos del archivo .env
    """
    try:
        conexion = psycopg2.connect(
            dbname=os.getenv("DB_NOMBRE", "postgres"),
            user=os.getenv("DB_USUARIO", "postgres"),
            password=os.getenv("DB_CONTRASENA", ""),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PUERTO", 5432),
            sslmode="require" if os.getenv(
                "DB_SSL", "false") == "true" else "disable"
        )
        return conexion

    except OperationalError as e:
        print("❌ Error al conectar con la base de datos:", e)
        raise


# 🔧 Prueba desde consola
if __name__ == '__main__':
    try:
        conexion = obtener_conexion()
        print("✅ Conexión establecida correctamente")
        conexion.close()
    except Exception as e:
        print("❌ Fallo al intentar conectar:", e)
