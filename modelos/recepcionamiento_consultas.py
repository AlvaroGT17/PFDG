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
