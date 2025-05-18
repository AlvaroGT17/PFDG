"""
Módulo de operaciones CRUD para la gestión de clientes.

Incluye funciones para:
- Crear, actualizar y eliminar clientes.
- Verificar existencia de DNI.
- Obtener información detallada o listada de clientes.
- Buscar clientes por nombre o ID.

Utiliza conexiones a PostgreSQL y fechas gestionadas con `datetime`.
"""
from modelos.conexion_bd import obtener_conexion
from psycopg2 import sql
from datetime import datetime
from utilidades.comprobar_dni import DNIUtils


def dni_ya_existe(dni):
    """
    Verifica si un DNI ya está registrado en la base de datos.

    Args:
        dni (str): DNI a verificar.

    Returns:
        bool: True si el DNI existe, False si no o si ocurre un error.
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
        print(f"Error comprobando DNI existente: {e}")
        return False


def crear_cliente(nombre, apellido1, apellido2, dni, telefono, email,
                  direccion, cp, localidad, provincia, observaciones):
    """
    Inserta un nuevo cliente en la base de datos.

    Args:
        nombre (str): Nombre del cliente.
        apellido1 (str): Primer apellido.
        apellido2 (str): Segundo apellido.
        dni (str): Documento Nacional de Identidad.
        telefono (str): Número de teléfono.
        email (str): Correo electrónico.
        direccion (str): Dirección postal.
        cp (str): Código postal.
        localidad (str): Ciudad/localidad.
        provincia (str): Provincia.
        observaciones (str): Comentarios u observaciones adicionales.

    Returns:
        bool: True si se creó correctamente, False si ocurrió un error.
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
        """)

        ahora = datetime.now()
        cursor.execute(consulta, (
            nombre.upper(),
            apellido1,
            apellido2,
            dni,
            telefono,
            email,
            direccion,
            cp,
            localidad,
            provincia,
            observaciones,
            ahora,
            ahora
        ))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al crear cliente: {e}")
        return False


def obtener_nombres_completos():
    """
    Devuelve una lista de nombres completos (nombre + apellidos) de todos los clientes.

    Returns:
        list[str]: Lista de nombres completos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT nombre || ' ' || primer_apellido || ' ' || COALESCE(segundo_apellido, '')
        FROM clientes
    """)
    resultados = [fila[0].strip() for fila in cursor.fetchall()]
    conexion.close()
    return resultados


def obtener_datos_cliente_por_nombre(nombre_completo):
    """
    Recupera todos los campos de un cliente a partir de su nombre completo.

    Args:
        nombre_completo (str): Nombre + apellidos del cliente.

    Returns:
        tuple or None: Tupla con los datos del cliente si se encuentra, None si no.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM clientes
        WHERE nombre || ' ' || primer_apellido || ' ' || COALESCE(segundo_apellido, '') = %s
    """, (nombre_completo,))
    cliente = cursor.fetchone()
    conexion.close()
    return cliente


def buscar_clientes_por_nombre():
    """
    Obtiene una lista de clientes con su nombre completo y ID, ordenados alfabéticamente.

    Returns:
        list[tuple]: Tuplas (nombre_completo, id).
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, primer_apellido, segundo_apellido
            FROM clientes
            ORDER BY nombre, primer_apellido, segundo_apellido
        """)
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()

        return [
            (f"{r[1]} {r[2]} {r[3]}".strip(), r[0])
            for r in resultados
        ]
    except Exception as e:
        print(f"Error al buscar clientes por nombre: {e}")
        return []


def obtener_cliente_por_id(cliente_id):
    """
    Recupera los datos de un cliente a partir de su ID.

    Args:
        cliente_id (int): ID del cliente.

    Returns:
        dict or None: Diccionario con los datos del cliente o None si no existe.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT nombre, primer_apellido, segundo_apellido, dni, telefono,
                   email, direccion, codigo_postal, localidad, provincia, observaciones
            FROM clientes
            WHERE id = %s
        """, (cliente_id,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado:
            return {
                "nombre": resultado[0],
                "primer_apellido": resultado[1],
                "segundo_apellido": resultado[2],
                "dni": resultado[3],
                "telefono": resultado[4],
                "email": resultado[5],
                "direccion": resultado[6],
                "codigo_postal": resultado[7],
                "localidad": resultado[8],
                "provincia": resultado[9],
                "observaciones": resultado[10],
            }
        return None
    except Exception as e:
        print(f"Error al obtener cliente por ID: {e}")
        return None


def obtener_clientes():
    """
    Devuelve una lista completa de todos los clientes en formato diccionario.

    Returns:
        list[dict]: Lista de todos los clientes con sus datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes")
    columnas = [col[0] for col in cursor.description]
    resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return resultados


def actualizar_cliente(cliente_id, nombre, apellido1, apellido2, dni, telefono, email,
                       direccion, cp, localidad, provincia, observaciones):
    """
    Actualiza los datos de un cliente existente.

    Args:
        cliente_id (int): ID del cliente a actualizar.
        (Los demás parámetros son los nuevos datos a aplicar.)

    Returns:
        bool: True si la actualización fue exitosa, False si falló.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = sql.SQL("""
            UPDATE clientes
            SET nombre = %s,
                primer_apellido = %s,
                segundo_apellido = %s,
                dni = %s,
                telefono = %s,
                email = %s,
                direccion = %s,
                codigo_postal = %s,
                localidad = %s,
                provincia = %s,
                observaciones = %s,
                updated_at = %s
            WHERE id = %s
        """)

        ahora = datetime.now()
        cursor.execute(consulta, (
            nombre.upper(),
            apellido1,
            apellido2,
            dni,
            telefono,
            email,
            direccion,
            cp,
            localidad,
            provincia,
            observaciones,
            ahora,
            cliente_id
        ))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
        return False


def eliminar_cliente_por_id(cliente_id):
    """
    Elimina un cliente de la base de datos por su ID.

    Args:
        cliente_id (int): ID del cliente a eliminar.

    Returns:
        bool: True si se eliminó correctamente, False si hubo error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")
        return False


def crear_cliente_y_devolver_id(nombre, apellido1, apellido2, dni, telefono, email,
                                direccion, cp, localidad, provincia, observaciones):
    """
    Crea un nuevo cliente y devuelve su ID generado automáticamente.

    Args:
        (Mismos que en crear_cliente)

    Returns:
        int or None: ID del cliente creado si tuvo éxito, o None si ocurrió un error.
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
            apellido1,
            apellido2,
            dni,
            telefono,
            email,
            direccion,
            cp,
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
        print(f"Error al crear cliente y devolver ID: {e}")
        return None
