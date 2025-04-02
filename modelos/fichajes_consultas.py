import psycopg2
from datetime import datetime
from modelos.conexion_bd import obtener_conexion


def registrar_fichaje(usuario_id, tipo):
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
