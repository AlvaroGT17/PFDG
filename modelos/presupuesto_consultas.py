from modelos.conexion_bd import obtener_conexion


def obtener_recepciones_para_presupuesto():
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
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tareas_presupuesto (presupuesto_id, descripcion, horas, precio_hora, total)
        VALUES (%s, %s, %s, %s, %s)
    """, (presupuesto_id, descripcion, horas, precio_hora, total))

    conn.commit()
    conn.close()
