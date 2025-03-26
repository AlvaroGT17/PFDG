import psycopg2
from psycopg2 import OperationalError


def obtener_conexion():
    """
    Devuelve una conexión activa a la base de datos de Supabase.
    Lanza un error si no se puede conectar.
    """
    try:
        conexion = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="AGT17021983BrfB",
            host="db.gxcexgzaavrffqqmwvxu.supabase.co",
            port=5432,
            sslmode="require"
        )
        return conexion

    except OperationalError as e:
        print("❌ Error al conectar con la base de datos:", e)
        raise


if __name__ == '__main__':
    try:
        conexion = obtener_conexion()
        print("✅ Conexión establecida correctamente")
        conexion.close()
    except Exception as e:
        print("❌ Fallo al intentar conectar:", e)
