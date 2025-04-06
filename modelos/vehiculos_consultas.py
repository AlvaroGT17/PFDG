from modelos.conexion_bd import obtener_conexion
from datetime import datetime


def buscar_vehiculo_por_matricula(matricula):
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
