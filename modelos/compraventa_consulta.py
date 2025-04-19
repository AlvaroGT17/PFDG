from modelos.conexion_bd import obtener_conexion


def obtener_vehiculos_disponibles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            matricula,
            marca,
            modelo,
            version,
            anio,
            bastidor,
            color,
            combustible,
            kilometros,
            potencia_cv,
            cambio,
            puertas,
            plazas,
            precio_compra,
            precio_venta,
            descuento_max,
            estado
        FROM coches_venta
        WHERE estado IN ('DISPONIBLE', 'RESERVADO')
    """)

    columnas = [col[0] for col in cursor.description]
    vehiculos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    conexion.close()
    return vehiculos
