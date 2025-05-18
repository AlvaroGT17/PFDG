"""
Módulo de gestión de fichajes de usuarios.

Incluye funciones para:
- Obtener el historial de fichajes personales de un usuario.
- Consultar todos los fichajes del sistema (modo administrador).
- Recuperar el nombre de un usuario a partir de su ID.

Todas las funciones acceden a la base de datos mediante `obtener_conexion`.
"""
from datetime import datetime
from modelos.conexion_bd import obtener_conexion


def obtener_fichajes_personales(usuario_id):
    """
    Recupera el historial de fichajes realizados por un usuario específico.

    Args:
        usuario_id (int): ID del usuario del que se desean obtener los fichajes.

    Returns:
        list[tuple]: Lista de tuplas con fecha/hora y tipo de fichaje ('Entrada' o 'Salida'),
        ordenadas de más reciente a más antigua.
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
    Recupera el historial completo de fichajes de todos los usuarios.

    Esta función está pensada para su uso por administradores del sistema.

    Returns:
        list[tuple]: Lista de tuplas con fecha/hora, tipo de fichaje y nombre del usuario.
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


def obtener_nombre_usuario(usuario_id):
    """
    Obtiene el nombre del usuario a partir de su ID.

    Args:
        usuario_id (int): Identificador del usuario.

    Returns:
        str: Nombre del usuario si existe, "Desconocido" si no se encuentra.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else "Desconocido"
    finally:
        cursor.close()
        conexion.close()
