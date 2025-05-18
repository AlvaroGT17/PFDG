"""
Módulo de gestión de vehículos en compraventa.

Permite realizar operaciones sobre la tabla `coches_venta` y registrar ventas asociadas
a clientes, incluyendo inserción, recuperación de datos y actualización del estado
del vehículo.

Funciones incluidas:
- obtener_vehiculos_disponibles
- insertar_nuevo_vehiculo
- obtener_id_cliente
- registrar_venta
"""
from datetime import datetime
from modelos.conexion_bd import obtener_conexion


def obtener_vehiculos_disponibles():
    """
    Recupera todos los vehículos que están disponibles o reservados para su venta.

    Returns:
        list[dict]: Lista de diccionarios con los datos de cada vehículo disponible o reservado.
    """
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
    """
    Inserta un nuevo vehículo en la tabla `coches_venta`.

    Args:
        datos (dict): Diccionario con los datos del vehículo, incluyendo:
            - marca, modelo, versión, año, matrícula, bastidor, color, etc.
            - información de compra y estado
            - cliente_id (opcional)
            - ruta de contrato y observaciones
    """
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
    """
    Recupera el ID de un cliente a partir de su DNI.

    Args:
        dni (str): DNI del cliente.

    Returns:
        int or None: ID del cliente si existe, o None si no se encuentra.
    """
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
    """
    Registra una venta de un vehículo a un cliente y actualiza el estado del vehículo a 'VENDIDO'.

    Args:
        cliente_id (int): ID del cliente que compra el vehículo.
        vehiculo_id (int): ID del vehículo vendido.
        precio_final (float): Precio final acordado de la venta.
        ruta_pdf (str): Ruta al archivo PDF generado del contrato.
        dir_contrato (str): Carpeta o directorio donde se encuentra el contrato.

    Raises:
        Exception: Si ocurre algún error durante la transacción, se revierte y lanza la excepción.
    """
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
