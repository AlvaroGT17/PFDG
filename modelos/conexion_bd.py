"""
Módulo de conexión a la base de datos PostgreSQL.

Utiliza variables de entorno definidas en un archivo `.env` para establecer
una conexión segura con la base de datos. Soporta conexión con o sin SSL
según la configuración establecida.

Funciones:
- obtener_conexion: Establece y devuelve una conexión activa a la base de datos.

Incluye un bloque de prueba para verificar la conexión directamente desde consola.
"""
import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env
load_dotenv()


def obtener_conexion():
    """
    Establece una conexión con la base de datos PostgreSQL usando las variables de entorno.

    Variables de entorno esperadas:
        - DB_NOMBRE: Nombre de la base de datos.
        - DB_USUARIO: Usuario de la base de datos.
        - DB_CONTRASENA: Contraseña del usuario.
        - DB_HOST: Dirección del servidor.
        - DB_PUERTO: Puerto de conexión.
        - DB_SSL: "true" para habilitar SSL, cualquier otro valor lo desactiva.

    Returns:
        connection (psycopg2.extensions.connection): Objeto de conexión a PostgreSQL.

    Raises:
        OperationalError: Si no se puede establecer la conexión.
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


# Prueba desde consola
if __name__ == '__main__':
    """
    Bloque de prueba para ejecutar el módulo directamente y verificar si la conexión es exitosa.
    """
    try:
        conexion = obtener_conexion()
        print("✅ Conexión establecida correctamente")
        conexion.close()
    except Exception as e:
        print("❌ Fallo al intentar conectar:", e)
