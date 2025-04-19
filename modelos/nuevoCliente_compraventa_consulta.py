from modelos.conexion_bd import obtener_conexion
from psycopg2 import sql
from datetime import datetime


def dni_ya_existe(dni):
    """
    Comprueba si ya existe un cliente con el mismo DNI.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM clientes WHERE dni = %s", (dni,))
        existe = cursor.fetchone() is not None
        cursor.close()
        conexion.close()
        return existe
    except Exception as e:
        print(f"❌ Error comprobando DNI existente: {e}")
        return False


def crear_cliente_y_devolver_id(nombre, primer_apellido, segundo_apellido, dni, telefono, email,
                                direccion, codigo_postal, localidad, provincia, observaciones):
    """
    Crea un nuevo cliente y devuelve su ID.

    Retorna:
        int | None
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = sql.SQL("""
            INSERT INTO clientes (
                nombre, primer_apellido, segundo_apellido, dni, telefono, email,
                direccion, codigo_postal, localidad, provincia, observaciones,
                created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """)

        ahora = datetime.now()
        cursor.execute(consulta, (
            nombre.upper(),
            primer_apellido.capitalize(),
            segundo_apellido.capitalize(),
            dni.upper(),
            telefono,
            email,
            direccion,
            codigo_postal,
            localidad,
            provincia,
            observaciones,
            ahora,
            ahora
        ))

        nuevo_id = cursor.fetchone()[0]
        conexion.commit()
        cursor.close()
        conexion.close()
        return nuevo_id
    except Exception as e:
        print(f"❌ Error al crear cliente y devolver ID: {e}")
        return None
