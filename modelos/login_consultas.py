"""
Módulo de autenticación y recuperación de cuentas.

Incluye funciones para:
- Obtener datos de usuario por nombre o email.
- Verificar contraseñas y códigos de recuperación.
- Guardar o actualizar contraseñas cifradas.
- Comprobar expiración de códigos OTP.

Requiere conexión a la base de datos PostgreSQL y el uso de la librería `bcrypt`
para cifrado y validación de contraseñas.
"""
import bcrypt
from psycopg2 import sql
from datetime import datetime, timedelta
from modelos.conexion_bd import obtener_conexion


def obtener_usuario_por_nombre(nombre: str):
    """
    Obtiene los datos de un usuario según su nombre en mayúsculas.

    Args:
        nombre (str): Nombre del usuario (no sensible a mayúsculas/minúsculas).

    Returns:
        dict or None: Diccionario con los datos del usuario y su rol si existe, None si no se encuentra.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = sql.SQL("""
            SELECT u.id, u.nombre, u.apellido, u.email, u.password, r.nombre AS rol
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.id
            WHERE UPPER(u.nombre) = %s
            LIMIT 1
        """)

        cursor.execute(consulta, (nombre.upper(),))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "id": resultado[0],
                "nombre": resultado[1],
                "apellido": resultado[2],
                "email": resultado[3],
                "password": resultado[4],
                "rol": resultado[5]
            }

    except Exception as e:
        print(f"❌ Error al consultar usuario: {e}")
    finally:
        if 'conexion' in locals():
            conexion.close()

    return None


def obtener_usuario_por_email(email: str):
    """
    Recupera el ID y nombre de un usuario a partir de su correo electrónico.

    Se utiliza principalmente para la recuperación de contraseña.

    Args:
        email (str): Dirección de correo electrónico del usuario.

    Returns:
        dict or None: Diccionario con ID y nombre si existe, None si no.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = sql.SQL("""
            SELECT id, nombre
            FROM usuarios
            WHERE LOWER(email) = LOWER(%s)
            LIMIT 1
        """)

        cursor.execute(consulta, (email,))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "id": resultado[0],
                "nombre": resultado[1]
            }

    except Exception as e:
        print(f"❌ Error al consultar usuario por email: {e}")
    finally:
        if 'conexion' in locals():
            conexion.close()

    return None


def guardar_codigo_recuperacion(usuario_id: int, codigo: str):
    """
    Guarda el código de recuperación generado y su fecha de expiración (5 minutos)
    para el usuario indicado.

    Args:
        usuario_id (int): ID del usuario.
        codigo (str): Código de recuperación (generalmente de 6 dígitos).

    Returns:
        bool: True si se guardó correctamente, False si ocurrió un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        expiracion = datetime.utcnow() + timedelta(minutes=5)

        consulta = sql.SQL("""
            UPDATE usuarios
            SET codigo_recuperacion = %s,
                expiracion_codigo = %s
            WHERE id = %s
        """)

        cursor.execute(consulta, (codigo, expiracion, usuario_id))
        conexion.commit()

        print(
            f"💾 Código de recuperación guardado correctamente para ID {usuario_id}")
        return True

    except Exception as e:
        print(f"❌ Error al guardar código de recuperación: {e}")
        return False

    finally:
        if 'conexion' in locals():
            conexion.close()


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """
    Compara una contraseña en texto plano con su versión cifrada usando bcrypt.

    Args:
        contrasena_plana (str): Contraseña ingresada por el usuario.
        contrasena_hash (str): Contraseña almacenada en la base de datos (cifrada).

    Returns:
        bool: True si coinciden, False si no.
    """
    return bcrypt.checkpw(contrasena_plana.encode("utf-8"), contrasena_hash.encode("utf-8"))


def verificar_codigo_recuperacion(email: str, codigo: str) -> bool:
    """
    Verifica que el código de recuperación sea válido para el usuario y no haya expirado.

    Args:
        email (str): Correo electrónico del usuario.
        codigo (str): Código de recuperación introducido.

    Returns:
        bool: True si el código es correcto y está vigente, False en caso contrario.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = """
            SELECT codigo_recuperacion, expiracion_codigo
            FROM usuarios
            WHERE email = %s
        """

        cursor.execute(consulta, (email,))
        resultado = cursor.fetchone()

        if resultado:
            codigo_guardado, expiracion = resultado

            if codigo == codigo_guardado and expiracion and datetime.utcnow() < expiracion:
                return True

    except Exception as e:
        print("❌ Error al verificar código:", e)

    finally:
        if 'conexion' in locals():
            conexion.close()

    return False


def actualizar_contrasena(email: str, nueva_contrasena: str) -> bool:
    """
    Cifra y actualiza la nueva contraseña de un usuario.

    También borra cualquier código de recuperación pendiente para ese usuario.

    Args:
        email (str): Correo del usuario a actualizar.
        nueva_contrasena (str): Nueva contraseña en texto plano.

    Returns:
        bool: True si se actualizó correctamente, False si ocurrió un error.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        hash_nueva = bcrypt.hashpw(nueva_contrasena.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("""
            UPDATE usuarios
            SET password = %s, codigo_recuperacion = NULL, expiracion_codigo = NULL
            WHERE email = %s
        """, (hash_nueva, email))

        conexion.commit()
        print(f"🔐 Contraseña actualizada correctamente para {email}")
        return True

    except Exception as e:
        print("❌ Error al actualizar contraseña:", e)
        return False

    finally:
        if 'conexion' in locals():
            conexion.close()


# Prueba desde consola
if __name__ == "__main__":
    """
    Permite probar el login por consola, solicitando nombre y contraseña.
    Solo se ejecuta si el archivo se ejecuta directamente.
    """
    print("🧪 Prueba de login por nombre de usuario")

    nombre = input("👤 Nombre de usuario: ")
    contrasena = input("🔐 Contraseña: ")

    usuario = obtener_usuario_por_nombre(nombre)

    if not usuario:
        print("❌ Usuario no encontrado.")
    elif verificar_contrasena(contrasena, usuario["password"]):
        print(
            f"✅ Login correcto. Bienvenido, {usuario['nombre']} ({usuario['rol']})")
    else:
        print("❌ Contraseña incorrecta.")
