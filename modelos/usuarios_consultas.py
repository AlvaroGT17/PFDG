"""
Módulo de gestión de usuarios y roles.

Incluye funciones para:
- Obtener los roles disponibles.
- Crear nuevos usuarios con contraseña cifrada.
- Verificar si un usuario existe por nombre o email.

Todas las operaciones utilizan la función `obtener_conexion()` para acceder
a la base de datos PostgreSQL y manejan errores de forma controlada.
"""
import bcrypt
import psycopg2
from psycopg2 import sql
from datetime import datetime
from modelos.conexion_bd import obtener_conexion


def obtener_roles():
    """
    Recupera todos los roles disponibles en la tabla `roles`.

    Returns:
        list[tuple]: Lista de tuplas (id, nombre) de los roles disponibles.
        Retorna una lista vacía si ocurre un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM roles ORDER BY id")
        roles = cursor.fetchall()
        cursor.close()
        conexion.close()
        return roles
    except Exception as e:
        print(f"Error al obtener roles: {e}")
        return []


def crear_usuario(nombre, apellido, email, contrasena, rol_id):
    """
    Crea un nuevo usuario en la base de datos.

    El nombre se almacena en mayúsculas y la contraseña se guarda cifrada
    usando bcrypt. También se registran las fechas de creación y actualización.

    Args:
        nombre (str): Nombre del usuario (se convierte a mayúsculas).
        apellido (str): Apellido del usuario.
        email (str): Correo electrónico del usuario.
        contrasena (str): Contraseña sin cifrar.
        rol_id (int): ID del rol asignado al usuario.

    Returns:
        bool: True si el usuario fue creado correctamente, False si hubo un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Convertir nombre a mayúsculas y cifrar contraseña
        nombre_mayus = nombre.upper()
        hashed_password = bcrypt.hashpw(
            contrasena.encode('utf-8'), bcrypt.gensalt())

        consulta = sql.SQL("""
            INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at, rol_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)

        ahora = datetime.now()
        cursor.execute(consulta, (
            nombre_mayus,
            apellido,
            email,
            hashed_password.decode('utf-8'),
            ahora,
            ahora,
            rol_id
        ))

        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False


def existe_usuario_por_nombre(nombre):
    """
    Verifica si existe un usuario con el nombre proporcionado.

    La comprobación se hace en mayúsculas para asegurar consistencia con la base de datos.

    Args:
        nombre (str): Nombre del usuario a verificar.

    Returns:
        bool: True si el usuario existe, False si no o si ocurre un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE nombre = %s", (nombre.upper(),))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado is not None
    except Exception as e:
        print(f"Error al comprobar existencia de usuario por nombre: {e}")
        return False


def existe_usuario_por_email(email):
    """
    Verifica si ya existe un usuario registrado con el email dado.

    Args:
        email (str): Dirección de correo electrónico a comprobar.

    Returns:
        bool: True si el email está registrado, False si no o si ocurre un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado is not None
    except Exception as e:
        print(f"Error al comprobar existencia de usuario por email: {e}")
        return False
