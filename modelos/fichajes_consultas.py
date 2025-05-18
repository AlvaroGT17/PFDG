"""
Módulo para registrar fichajes de entrada y salida del personal.

Incluye una única función para insertar registros en la tabla `fichajes`,
registrando el ID del usuario, el tipo de fichaje y la fecha/hora actual.
"""
import psycopg2
from datetime import datetime
from modelos.conexion_bd import obtener_conexion


def registrar_fichaje(usuario_id, tipo):
    """
    Registra un nuevo fichaje (entrada o salida) en la base de datos.

    Args:
        usuario_id (int): ID del usuario que realiza el fichaje.
        tipo (str): Tipo de fichaje, normalmente "Entrada" o "Salida".

    La función guarda automáticamente la fecha y hora del fichaje
    en el momento de la ejecución.
    """
    conexion = obtener_conexion()
    try:
        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO fichajes (usuario_id, tipo, fecha_hora)
                    VALUES (%s, %s, %s)
                """, (usuario_id, tipo, datetime.now()))
    finally:
        conexion.close()
