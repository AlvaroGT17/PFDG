from datetime import datetime
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


def insertar_nuevo_vehiculo(datos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO coches_venta (
            marca, modelo, version, anio, matricula, bastidor, color, combustible,
            kilometros, potencia_cv, cambio, puertas, plazas, precio_compra,
            precio_venta, descuento_maximo, estado, origen_compra, cliente_id,
            observaciones, descuento_max, dir_contrato
        )
        VALUES (
            %(marca)s, %(modelo)s, %(version)s, %(anio)s, %(matricula)s, %(bastidor)s, %(color)s, %(combustible)s,
            %(kilometros)s, %(potencia_cv)s, %(cambio)s, %(puertas)s, %(plazas)s, %(precio_compra)s,
            %(precio_venta)s, %(descuento_maximo)s, %(estado)s, %(origen_compra)s, %(cliente_id)s,
            %(observaciones)s, %(descuento_max)s, %(dir_contrato)s
        )
    """
    cursor.execute(consulta, datos)
    conexion.commit()
    cursor.close()
    conexion.close()


def obtener_id_cliente(dni):
    if not dni:
        return None
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM clientes WHERE dni = %s", (dni,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado[0] if resultado else None


def registrar_venta(cliente_id, vehiculo_id, precio_final, ruta_pdf, dir_contrato):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # 1. Insertar la venta
        cursor.execute("""
            INSERT INTO ventas (cliente_id, vehiculo_id, precio_final, ruta_pdf, dir_contrato)
            VALUES (%s, %s, %s, %s, %s)
        """, (cliente_id, vehiculo_id, precio_final, ruta_pdf, dir_contrato))

        # 2. Actualizar el estado del vehículo a 'VENDIDO'
        cursor.execute("""
            UPDATE coches_venta
            SET estado = 'VENDIDO'
            WHERE id = %s
        """, (vehiculo_id,))

        conexion.commit()

    except Exception as e:
        conexion.rollback()
        raise e

    finally:
        cursor.close()
        conexion.close()
