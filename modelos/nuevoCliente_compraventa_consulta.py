"""
Módulo de operaciones relacionadas con la gestión de clientes.

Proporciona funciones para:
- Comprobar si un cliente ya existe por su DNI.
- Crear un nuevo cliente y obtener su ID.
- Buscar clientes por nombre completo, ID o DNI.
- Recuperar los datos completos de un cliente en forma de diccionario.
"""
from modelos.conexion_bd import obtener_conexion
from psycopg2 import sql
from datetime import datetime


def dni_ya_existe(dni):
    """
    Crea un nuevo cliente en la base de datos y devuelve su ID.

    Los campos nombre y apellidos se normalizan (mayúsculas y capitalización).
    También se registran las fechas de creación y actualización.

    Args:
        nombre (str): Nombre del cliente.
        primer_apellido (str): Primer apellido.
        segundo_apellido (str): Segundo apellido.
        dni (str): DNI del cliente.
        telefono (str): Teléfono de contacto.
        email (str): Correo electrónico.
        direccion (str): Dirección completa.
        codigo_postal (str): Código postal.
        localidad (str): Ciudad o localidad.
        provincia (str): Provincia.
        observaciones (str): Comentarios u observaciones adicionales.

    Returns:
        int or None: ID del nuevo cliente si se creó correctamente, None si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM clientes WHERE dni = %s", (dni,))
        existe = cursor.fetchone() is not None
        cursor.close()
        conexion.close()
        return existe
    except Exception as e:
        print(f"❌ Error comprobando DNI existente: {e}")
        return False


def crear_cliente_y_devolver_id(nombre, primer_apellido, segundo_apellido, dni, telefono, email,
                                direccion, codigo_postal, localidad, provincia, observaciones):
    """
    Busca un cliente por su nombre completo (nombre + apellidos).

    La búsqueda se hace en mayúsculas y concatenando nombre, primer y segundo apellido.

    Args:
        nombre_completo (str): Nombre completo del cliente (sin acentos ni diferencias de mayúsculas/minúsculas).

    Returns:
        tuple or None: Tupla con los datos del cliente si se encuentra, None si no existe o hay error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = sql.SQL("""
            INSERT INTO clientes (
                nombre, primer_apellido, segundo_apellido, dni, telefono, email,
                direccion, codigo_postal, localidad, provincia, observaciones,
                created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """)

        ahora = datetime.now()
        cursor.execute(consulta, (
            nombre.upper(),
            primer_apellido.capitalize(),
            segundo_apellido.capitalize(),
            dni.upper(),
            telefono,
            email,
            direccion,
            codigo_postal,
            localidad,
            provincia,
            observaciones,
            ahora,
            ahora
        ))

        nuevo_id = cursor.fetchone()[0]
        conexion.commit()
        cursor.close()
        conexion.close()
        return nuevo_id
    except Exception as e:
        print(f"❌ Error al crear cliente y devolver ID: {e}")
        return None


def obtener_datos_cliente_por_nombre(nombre_completo):
    """
    Obtiene los datos completos de un cliente a partir de su ID.

    Args:
        cliente_id (int): ID del cliente a buscar.

    Returns:
        dict or None: Diccionario con los datos del cliente si se encuentra, None si no existe.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = sql.SQL("""
            SELECT * FROM clientes
            WHERE UPPER(nombre || ' ' || primer_apellido || ' ' || segundo_apellido) = %s
            LIMIT 1
        """)
        cursor.execute(consulta, (nombre_completo.upper(),))
        cliente = cursor.fetchone()

        cursor.close()
        conexion.close()
        return cliente
    except Exception as e:
        print(f"❌ Error al obtener cliente por nombre: {e}")
        return None


def obtener_cliente_por_id(cliente_id):
    """
    Obtiene los datos completos de un cliente a partir de su DNI.

    Args:
        dni (str): DNI del cliente a buscar.

    Returns:
        dict or None: Diccionario con los datos del cliente si se encuentra, None si no existe.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = sql.SQL("""
            SELECT id, nombre, primer_apellido, segundo_apellido, dni, telefono,
                   email, direccion, codigo_postal, localidad, provincia, observaciones
            FROM clientes
            WHERE id = %s
        """)
        cursor.execute(consulta, (cliente_id,))
        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            claves = ["id", "nombre", "primer_apellido", "segundo_apellido", "dni", "telefono",
                      "email", "direccion", "codigo_postal", "localidad", "provincia", "observaciones"]
            return dict(zip(claves, fila))
        else:
            return None
    except Exception as e:
        print(f"❌ Error al obtener cliente por ID: {e}")
        return None


def obtener_cliente_por_id_por_dni(dni):
    """
    Devuelve un diccionario con los datos del cliente según su DNI.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, primer_apellido, segundo_apellido, dni, telefono,
                   email, direccion, codigo_postal, localidad, provincia, observaciones
            FROM clientes
            WHERE dni = %s
            LIMIT 1
        """, (dni,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()

        if fila:
            claves = ["id", "nombre", "primer_apellido", "segundo_apellido", "dni", "telefono",
                      "email", "direccion", "codigo_postal", "localidad", "provincia", "observaciones"]
            return dict(zip(claves, fila))
        else:
            return None
    except Exception as e:
        print(f"❌ Error al obtener cliente por DNI: {e}")
        return None
