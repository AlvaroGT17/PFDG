from datetime import datetime
from modelos.conexion_bd import obtener_conexion


def obtener_fichajes_personales(usuario_id):
    """
    Devuelve una lista de fichajes del usuario actual.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT fecha_hora, tipo
            FROM fichajes
            WHERE usuario_id = %s
            ORDER BY fecha_hora DESC
        """, (usuario_id,))
        resultados = cursor.fetchall()
        return resultados

    finally:
        cursor.close()
        conexion.close()


def obtener_fichajes_globales():
    """
    Devuelve una lista de todos los fichajes, incluyendo nombre del usuario.
    Solo para administrador.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT f.fecha_hora, f.tipo, u.nombre
            FROM fichajes f
            JOIN usuarios u ON f.usuario_id = u.id
            ORDER BY f.fecha_hora DESC
        """)
        resultados = cursor.fetchall()
        return resultados

    finally:
        cursor.close()
        conexion.close()
