import psycopg2
from modelos.conexion_bd import obtener_conexion


def obtener_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT nombre, primer_apellido, segundo_apellido, dni, telefono, email, direccion
        FROM clientes
    """)
    columnas = [desc[0] for desc in cursor.description]
    resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return resultados


def obtener_matriculas():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT matricula FROM vehiculos")
        resultados = [fila[0].strip().upper() for fila in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        print(f"Error al obtener matrículas: {e}")
        return []


def obtener_datos_vehiculo_por_matricula(matricula):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT v.marca, v.modelo, v.color, v.anyo, v.combustible, v.numero_bastidor, 
                   t.categoria, t.nombre
            FROM vehiculos v
            LEFT JOIN tipos_vehiculo t ON v.tipo_vehiculo = t.id
            WHERE UPPER(v.matricula) = %s
        """, (matricula.upper(),))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado:
            return {
                "marca": resultado[0],
                "modelo": resultado[1],
                "color": resultado[2],
                "anio": resultado[3],
                "kilometros": '',  # si no estás usando este dato, lo dejas así
                "combustible": resultado[4],
                "numero_bastidor": resultado[5],
                "categoria": resultado[6],
                "tipo": resultado[7]
            }
        return None
    except Exception as e:
        print(f"Error al obtener datos del vehículo: {e}")
        return None


def obtener_categorias_vehiculo():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT DISTINCT categoria FROM tipos_vehiculo ORDER BY categoria")
    resultados = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return resultados


def obtener_tipos_vehiculo():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT categoria, nombre FROM tipos_vehiculo ORDER BY categoria, nombre")
    resultados = [{"categoria": fila[0], "nombre": fila[1]}
                  for fila in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return resultados


def obtener_combustibles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM combustibles ORDER BY id")
    resultados = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return resultados


def obtener_matriculas_existentes():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT matricula FROM vehiculos")
        resultados = [fila[0] for fila in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        print(f"Error al obtener matrículas: {e}")
        return []


def obtener_matriculas_por_cliente(dni_cliente):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT v.matricula
            FROM vehiculos v
            JOIN clientes c ON v.cliente_id = c.id
            WHERE UPPER(c.dni) = %s
        """, (dni_cliente.upper(),))
        resultado = [fila[0] for fila in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error al obtener matrículas del cliente: {e}")
        return []


def obtener_siguiente_numero_recepcionamiento():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT MAX(num_recepcionamiento) FROM recepcionamientos")
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado and resultado[0]:
            return int(resultado[0]) + 1
        else:
            return 1  # Si no hay registros aún
    except Exception as e:
        print(f"Error al obtener el siguiente número de recepcionamiento: {e}")
        return 1


def obtener_motivos():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM tipos_intervencion ORDER BY id")
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [{"id": fila[0], "nombre": fila[1]} for fila in resultados]
    except Exception as e:
        print(f"Error al obtener motivos: {e}")
        return []


def obtener_urgencias():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, descripcion FROM urgencias ORDER BY id")
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [{"id": fila[0], "descripcion": fila[1]} for fila in resultados]
    except Exception as e:
        print(f"Error al obtener urgencias: {e}")
        return []


def obtener_datos_completos_recepcionamiento():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT 'motivo' AS tipo, id, nombre FROM tipos_intervencion
            UNION ALL
            SELECT 'urgencia', id, descripcion FROM urgencias
            UNION ALL
            SELECT 'categoria', NULL AS id, categoria FROM (
                SELECT DISTINCT categoria FROM tipos_vehiculo
            ) AS sub
            UNION ALL
            SELECT 'tipo', NULL, nombre FROM tipos_vehiculo
            UNION ALL
            SELECT 'combustible', NULL, nombre FROM combustibles
        """)

        resultados = cursor.fetchall()

        datos = {
            "motivos": [],
            "urgencias": [],
            "categorias": [],
            "tipos": [],
            "combustibles": []
        }

        for tipo, id_valor, nombre in resultados:
            if tipo == "motivo":
                datos["motivos"].append({"id": id_valor, "nombre": nombre})
            elif tipo == "urgencia":
                datos["urgencias"].append(
                    {"id": id_valor, "descripcion": nombre})
            elif tipo == "categoria":
                datos["categorias"].append(nombre)
            elif tipo == "tipo":
                # Puedes añadir más si quieres categoría
                datos["tipos"].append({"nombre": nombre})
            elif tipo == "combustible":
                datos["combustibles"].append(nombre)

        cursor.close()
        conexion.close()
        return datos
    except Exception as e:
        print(f"Error al obtener datos completos de recepcionamiento: {e}")
        return {
            "motivos": [],
            "urgencias": [],
            "categorias": [],
            "tipos": [],
            "combustibles": []
        }
