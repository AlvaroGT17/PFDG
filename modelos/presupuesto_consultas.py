"""
Módulo para la gestión de presupuestos en base a recepcionamientos.

Incluye funciones para:
- Obtener recepcionamientos pendientes de presupuesto.
- Insertar presupuestos nuevos.
- Registrar tareas asociadas a cada presupuesto.
"""
from modelos.conexion_bd import obtener_conexion


def obtener_recepciones_para_presupuesto():
    """
    Recupera los recepcionamientos que aún no tienen un presupuesto asignado.

    Returns:
        list[dict]: Lista de diccionarios con datos del recepcionamiento,
        incluyendo cliente, correo, matrícula, observaciones y precio máximo autorizado.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()

    query = """
    SELECT 
        r.id,
        r.num_recepcionamiento,
        r.fecha,
        r.acepta_reparacion_hasta AS precio_max_autorizado,
        r.observaciones_generales AS observaciones,
        c.nombre AS cliente,
        c.email AS correo_cliente,
        v.matricula
    FROM recepcionamientos r
    JOIN clientes c ON c.id = r.cliente_id
    JOIN vehiculos v ON v.id = r.vehiculo_id
    WHERE NOT EXISTS (
        SELECT 1 FROM presupuestos p WHERE p.recepcion_id = r.id
    )
    ORDER BY r.id DESC
    """

    cursor.execute(query)
    columnas = [col[0] for col in cursor.description]
    resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    conn.close()
    return resultados


def insertar_presupuesto(recepcion_id, total, respuesta, ruta_pdf):
    """
    Inserta un nuevo presupuesto asociado a un recepcionamiento existente.

    Args:
        recepcion_id (int): ID del recepcionamiento al que se asocia el presupuesto.
        total (float): Total estimado del presupuesto.
        respuesta (str): Respuesta del cliente (puede ser "Pendiente", "Aceptado", etc.).
        ruta_pdf (str): Ruta del documento PDF generado.

    Returns:
        int: ID del nuevo presupuesto insertado.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO presupuestos (recepcion_id, total_estimado, respuesta_cliente, fecha_creacion, ruta_pdf)
        VALUES (%s, %s, %s, NOW(), %s)
        RETURNING id
    """, (recepcion_id, total, respuesta, ruta_pdf))

    presupuesto_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return presupuesto_id


def insertar_tarea_presupuesto(presupuesto_id, descripcion, horas, precio_hora, total):
    """
    Inserta una tarea individual asociada a un presupuesto determinado.

    Args:
        presupuesto_id (int): ID del presupuesto al que pertenece la tarea.
        descripcion (str): Descripción de la tarea.
        horas (float): Cantidad de horas estimadas.
        precio_hora (float): Precio por hora de la tarea.
        total (float): Coste total de la tarea.

    Returns:
        None
    """
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tareas_presupuesto (presupuesto_id, descripcion, horas, precio_hora, total)
        VALUES (%s, %s, %s, %s, %s)
    """, (presupuesto_id, descripcion, horas, precio_hora, total))

    conn.commit()
    conn.close()
