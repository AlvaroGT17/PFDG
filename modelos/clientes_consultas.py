from modelos.conexion_bd import obtener_conexion
from psycopg2 import sql
from datetime import datetime


def dni_ya_existe(dni):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM clientes WHERE dni = %s", (dni,))
        existe = cursor.fetchone() is not None
        cursor.close()
        conexion.close()
        return existe
    except Exception as e:
        print(f"Error comprobando DNI existente: {e}")
        return False


def crear_cliente(nombre, apellido1, apellido2, dni, telefono, email,
                  direccion, cp, localidad, provincia, observaciones):
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
        """)

        ahora = datetime.now()
        cursor.execute(consulta, (
            nombre.upper(),
            apellido1,
            apellido2,
            dni,
            telefono,
            email,
            direccion,
            cp,
            localidad,
            provincia,
            observaciones,
            ahora,
            ahora
        ))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al crear cliente: {e}")
        return False
