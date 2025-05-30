"""
Módulo de consultas y operaciones relacionadas con clientes, vehículos y recepcionamientos.

Incluye funciones para:
- Obtener información de clientes y vehículos.
- Consultar categorías, tipos y combustibles.
- Verificar datos existentes por DNI o matrícula.
- Generar y guardar recepcionamientos en la base de datos.
"""
import psycopg2
from modelos.conexion_bd import obtener_conexion


def obtener_clientes():
    """
    Obtiene todos los clientes registrados en la base de datos.

    Returns:
        list[dict]: Lista de clientes con campos como nombre, apellidos, DNI, teléfono, etc.
    """
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
    """
    Recupera todas las matrículas de vehículos registradas, en mayúsculas y sin espacios.

    Returns:
        list[str]: Lista de matrículas.
    """
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
    """
    Obtiene los datos detallados de un vehículo según su matrícula.

    Args:
        matricula (str): Matrícula del vehículo a buscar.

    Returns:
        dict or None: Diccionario con datos del vehículo si se encuentra, None en caso contrario.
    """
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
    """
    Devuelve una lista de categorías distintas de vehículo.

    Returns:
        list[str]: Lista de nombres de categorías.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT DISTINCT categoria FROM tipos_vehiculo ORDER BY categoria")
    resultados = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return resultados


def obtener_tipos_vehiculo():
    """
    Devuelve una lista de tipos de vehículo con su categoría asociada.

    Returns:
        list[dict]: Lista de diccionarios con categoría y tipo de vehículo.
    """
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
    """
    Recupera todos los nombres de combustibles disponibles.

    Returns:
        list[str]: Lista de combustibles.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM combustibles ORDER BY id")
    resultados = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return resultados


def obtener_matriculas_existentes():
    """
    Devuelve todas las matrículas registradas en la base de datos.

    Returns:
        list[str]: Lista de matrículas existentes.
    """
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
    """
    Devuelve todas las matrículas asociadas a un cliente dado su DNI.

    Args:
        dni_cliente (str): DNI del cliente.

    Returns:
        list[str]: Lista de matrículas vinculadas al cliente.
    """
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
    """
    Calcula el siguiente número disponible para un nuevo recepcionamiento.

    Returns:
        int: Número siguiente para recepcionamiento (inicia en 1 si no hay registros).
    """
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
    """
    Obtiene los motivos de intervención disponibles.

    Returns:
        list[dict]: Lista de motivos con sus IDs y nombres.
    """
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
    """
    Obtiene los niveles de urgencia registrados.

    Returns:
        list[dict]: Lista con ID y descripción de cada urgencia.
    """
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
    """
    Obtiene todos los datos necesarios para completar un formulario de recepcionamiento,
    incluyendo motivos, urgencias, categorías, tipos y combustibles.

    Returns:
        dict: Diccionario con claves 'motivos', 'urgencias', 'categorias', 'tipos' y 'combustibles'.
    """
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


def obtener_cliente_id_por_dni(dni):
    """
    Recupera el ID de cliente a partir de su DNI.

    Args:
        dni (str): DNI del cliente.

    Returns:
        int or None: ID del cliente si existe, None en caso contrario.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id FROM clientes WHERE UPPER(dni) = %s", (dni.upper(),))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener cliente_id: {e}")
        return None


def obtener_vehiculo_id_por_matricula(matricula):
    """
    Recupera el ID de un vehículo a partir de su matrícula.

    Args:
        matricula (str): Matrícula del vehículo.

    Returns:
        int or None: ID del vehículo si existe, None en caso contrario.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id FROM vehiculos WHERE UPPER(matricula) = %s", (matricula.upper(),))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener vehiculo_id: {e}")
        return None


def obtener_estado_id_por_defecto():
    """
    Obtiene el ID del estado por defecto (normalmente 'Pendiente') para intervenciones.

    Returns:
        int or None: ID del estado si existe, None si no se encuentra.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id FROM estados_intervencion WHERE nombre ILIKE 'pendiente' LIMIT 1"
        )
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener estado por defecto: {e}")
        return None


def insertar_recepcionamiento_en_bd(datos):
    """
    Inserta un nuevo registro de recepcionamiento en la base de datos.

    Args:
        datos (dict): Diccionario con todos los datos necesarios del formulario de recepción.

    Returns:
        tuple: (True, None) si fue exitoso, o (False, error_str) si ocurrió un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO recepcionamientos (
                urgencia_id,
                cliente_id,
                vehiculo_id,
                usuario_id,
                estado_id,
                fecha,
                itv_en_vigor,
                ultima_revision,
                desea_presupuesto_por_escrito,
                entregar_impreso,
                enviar_por_correo,
                num_recepcionamiento,
                arranca,
                viene_con_grua,
                tiene_seguro,
                acepta_reparacion_hasta,
                valor_estimado,
                motivo_id,
                estado_interior,
                observaciones_generales,
                ruta_documento,
                compania_seguro,
                lista_averias_cliente,
                estado_exterior
            ) VALUES (
                %(urgencia_id)s,
                %(cliente_id)s,
                %(vehiculo_id)s,
                %(usuario_id)s,
                %(estado_id)s,
                NOW(),
                %(itv)s,
                %(ultima_revision)s,
                %(desea_presupuesto)s,
                %(entregar_impreso)s,
                %(enviar_correo)s,
                %(numero_recepcionamiento)s,
                %(arranca)s,
                %(grua)s,
                %(seguro)s,
                %(reparacion_hasta)s,
                %(valor_estimado)s,
                %(motivo_id)s,
                %(estado_interior)s,
                %(observaciones)s,
                %(ruta_pdf)s,
                %(compania_seguro)s,
                %(lista_averias)s,
                %(estado_exterior)s
            )
        """, {
            "urgencia_id": datos["urgencia_id"],
            "cliente_id": datos["cliente_id"],
            "vehiculo_id": datos["vehiculo_id"],
            "usuario_id": datos["usuario_id"],
            "estado_id": datos["estado_id"],
            "itv": datos["itv"],
            "ultima_revision": datos["ultima_revision"] or None,
            "desea_presupuesto": datos["desea_presupuesto"],
            "entregar_impreso": datos.get("entregar_impreso", False),
            "enviar_correo": datos.get("enviar_correo", False),
            "numero_recepcionamiento": datos["numero_recepcionamiento"],
            "arranca": datos["arranca"],
            "grua": datos["grua"],
            "seguro": datos["seguro"],
            "reparacion_hasta": datos["reparacion_hasta"] or 0,
            "valor_estimado": datos["valor_estimado"] or 0,
            "motivo_id": datos["motivo_id"],
            "estado_interior": datos["estado_interior"],
            "observaciones": datos["observaciones"],
            "ruta_pdf": datos["ruta_pdf"],
            "compania_seguro": datos["compania_seguro"],
            "lista_averias": datos.get("lista_averias", "Sin especificar"),
            "estado_exterior": datos["estado_exterior"]
        })

        conexion.commit()
        cursor.close()
        conexion.close()
        return True, None

    except Exception as e:
        return False, str(e)
