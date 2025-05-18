"""
Módulo de consultas relacionadas con vehículos.

Proporciona funciones para buscar, crear, modificar y eliminar registros
de vehículos en la base de datos, así como obtener datos auxiliares
como tipos de vehículo, combustibles y categorías.

Todas las operaciones utilizan la conexión proporcionada por `obtener_conexion`
y gestionan errores de forma controlada.
"""

from modelos.conexion_bd import obtener_conexion
from datetime import datetime


def buscar_vehiculo_por_matricula(matricula):
    """
    Busca un vehículo en la base de datos a partir de su matrícula.

    Args:
        matricula (str): Matrícula del vehículo a buscar.

    Returns:
        dict or None: Diccionario con los datos del vehículo si se encuentra,
        o None si no existe.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT v.id, v.matricula, v.marca, v.modelo, v.color, v.anyo,
                   v.tipo_vehiculo, v.cliente_id, v.observaciones,
                   t.nombre AS tipo_nombre, t.categoria,
                   v.numero_bastidor, c.nombre AS combustible_nombre, v.combustible_id
            FROM vehiculos v
            JOIN tipos_vehiculo t ON v.tipo_vehiculo = t.id
            LEFT JOIN combustibles c ON v.combustible_id = c.id
            WHERE v.matricula = %s
        """, (matricula,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()

        if fila:
            return {
                "id": fila[0],
                "matricula": fila[1],
                "marca": fila[2],
                "modelo": fila[3],
                "color": fila[4],
                "anyo": fila[5],
                "tipo_vehiculo_id": fila[6],
                "cliente_id": fila[7],
                "observaciones": fila[8],
                "tipo_nombre": fila[9],
                "categoria": fila[10],
                "numero_bastidor": fila[11],
                "combustible": fila[12],
                "combustible_id": fila[13]
            }
        return None
    except Exception as e:
        print(f"Error al buscar vehículo: {e}")
        return None


def obtener_combustibles():
    """
    Recupera todos los combustibles registrados en la base de datos.

    Returns:
        list[dict]: Lista de diccionarios con los combustibles (id y nombre).
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM combustibles ORDER BY nombre")
        resultado = [{"id": fila[0], "nombre": fila[1]}
                     for fila in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error al obtener combustibles: {e}")
        return []


def obtener_matriculas_existentes():
    """
    Obtiene todas las matrículas de vehículos registradas en la base de datos.

    Returns:
        list[str]: Lista de matrículas ordenadas alfabéticamente.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT matricula FROM vehiculos ORDER BY matricula")
        matriculas = [fila[0] for fila in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return matriculas
    except Exception as e:
        print(f"Error al obtener matrículas existentes: {e}")
        return []


def matricula_ya_existe(matricula, excluir_id=None):
    """
    Verifica si una matrícula ya está registrada, opcionalmente excluyendo un vehículo por ID.

    Args:
        matricula (str): Matrícula a verificar.
        excluir_id (int, optional): ID de un vehículo a excluir de la comprobación.

    Returns:
        bool: True si la matrícula ya existe, False en caso contrario.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        if excluir_id:
            cursor.execute("""
                SELECT 1 FROM vehiculos
                WHERE matricula = %s AND id != %s
            """, (matricula, excluir_id))
        else:
            cursor.execute("""
                SELECT 1 FROM vehiculos
                WHERE matricula = %s
            """, (matricula,))
        existe = cursor.fetchone() is not None
        cursor.close()
        conexion.close()
        return existe
    except Exception as e:
        print(f"Error comprobando matrícula existente: {e}")
        return False


def crear_vehiculo(matricula, marca, modelo, color, tipo_vehiculo, cliente_id,
                   numero_bastidor, combustible_id, anyo, observaciones=None):
    """
    Inserta un nuevo vehículo en la base de datos.

    Args:
        matricula (str): Matrícula del vehículo.
        marca (str): Marca del vehículo.
        modelo (str): Modelo del vehículo.
        color (str): Color del vehículo.
        tipo_vehiculo (int): ID del tipo de vehículo.
        cliente_id (int): ID del cliente asociado.
        numero_bastidor (str): Número de bastidor del vehículo.
        combustible_id (int): ID del tipo de combustible.
        anyo (int): Año de matriculación o fabricación.
        observaciones (str, optional): Comentarios adicionales.

    Returns:
        bool: True si se creó correctamente, False si hubo un error o matrícula duplicada.
    """
    try:
        if matricula_ya_existe(matricula):
            return False

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO vehiculos (
                matricula, marca, modelo, color, tipo_vehiculo,
                cliente_id, numero_bastidor, combustible_id, anyo,
                observaciones, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            matricula, marca, modelo, color, tipo_vehiculo,
            cliente_id, numero_bastidor, combustible_id, anyo,
            observaciones, datetime.now(), datetime.now()
        ))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al crear vehículo: {e}")
        return False


def modificar_vehiculo(vehiculo_id, matricula, marca, modelo, color, tipo_vehiculo,
                       cliente_id, numero_bastidor, combustible_id, anyo, observaciones=None):
    """
    Actualiza los datos de un vehículo existente.

    Args:
        vehiculo_id (int): ID del vehículo a modificar.
        matricula (str): Nueva matrícula.
        marca (str): Nueva marca.
        modelo (str): Nuevo modelo.
        color (str): Nuevo color.
        tipo_vehiculo (int): ID del nuevo tipo de vehículo.
        cliente_id (int): ID del cliente.
        numero_bastidor (str): Nuevo número de bastidor.
        combustible_id (int): ID del nuevo combustible.
        anyo (int): Año de matriculación o fabricación.
        observaciones (str, optional): Nuevas observaciones.

    Returns:
        bool: True si la modificación fue exitosa, False si falló o la matrícula ya existe.
    """
    try:
        if matricula_ya_existe(matricula, excluir_id=vehiculo_id):
            return False

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE vehiculos SET
                matricula = %s,
                marca = %s,
                modelo = %s,
                color = %s,
                tipo_vehiculo = %s,
                cliente_id = %s,
                numero_bastidor = %s,
                combustible_id = %s,
                anyo = %s,
                observaciones = %s,
                updated_at = %s
            WHERE id = %s
        """, (
            matricula, marca, modelo, color, tipo_vehiculo,
            cliente_id, numero_bastidor, combustible_id, anyo,
            observaciones, datetime.now(), vehiculo_id
        ))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al modificar vehículo: {e}")
        return False


def eliminar_vehiculo(vehiculo_id):
    """
    Elimina un vehículo de la base de datos por su ID.

    Args:
        vehiculo_id (int): ID del vehículo a eliminar.

    Returns:
        bool: True si se eliminó correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM vehiculos WHERE id = %s", (vehiculo_id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al eliminar vehículo: {e}")
        return False


def obtener_tipos_vehiculo_con_categoria():
    """
    Obtiene todos los tipos de vehículo registrados junto con su categoría.

    Returns:
        list[dict]: Lista de tipos con sus IDs, nombres y categorías.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre AS tipo, categoria
            FROM tipos_vehiculo
            ORDER BY categoria, tipo
        """)
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()

        return [
            {"id": fila[0], "tipo": fila[1], "categoria": fila[2]}
            for fila in filas
        ]
    except Exception as e:
        print(f"Error al obtener tipos de vehículo: {e}")
        return []


def obtener_tipos_por_categoria(categoria):
    """
    Obtiene todos los tipos de vehículo correspondientes a una categoría dada.

    Args:
        categoria (str): Nombre de la categoría.

    Returns:
        list[str]: Lista de nombres de tipos de vehículo pertenecientes a la categoría.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT nombre
            FROM tipos_vehiculo
            WHERE categoria = %s
            ORDER BY nombre
        """, (categoria,))
        tipos = [fila[0] for fila in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return tipos
    except Exception as e:
        print(f"Error al obtener tipos por categoría: {e}")
        return []


def obtener_categorias():
    """
    Recupera todas las categorías de vehículos registradas en el sistema.

    Returns:
        list[str]: Lista de nombres de categorías, sin duplicados.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT DISTINCT categoria FROM tipos_vehiculo ORDER BY categoria")
        categorias = [fila[0] for fila in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return categorias
    except Exception as e:
        print(f"Error al obtener categorías: {e}")
        return []
