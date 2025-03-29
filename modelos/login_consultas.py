import bcrypt
from psycopg2 import sql
from datetime import datetime, timedelta
from modelos.conexion_bd import obtener_conexion


def obtener_usuario_por_nombre(nombre: str):
    """
    Devuelve los datos del usuario con ese nombre (en mayúsculas),
    o None si no existe. Se usa para login.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = sql.SQL("""
            SELECT id, nombre, apellido, email, password, rol
            FROM usuarios
            WHERE UPPER(nombre) = %s
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
                "password": resultado[4],  # hash
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
    Devuelve los datos básicos del usuario por email (id y nombre).
    Se usa para recuperación de cuenta.
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
    Guarda el código de recuperación y su tiempo de expiración
    para el usuario especificado.
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
    return bcrypt.checkpw(contrasena_plana.encode("utf-8"), contrasena_hash.encode("utf-8"))


def verificar_codigo_recuperacion(email: str, codigo: str) -> bool:
    """
    Verifica si el código de recuperación es válido para el correo dado
    y si no ha expirado.
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
    Actualiza la contraseña de un usuario en la base de datos, cifrándola con bcrypt.
    Devuelve True si fue exitoso, False en caso contrario.
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


# 🔧 Prueba desde consola
if __name__ == "__main__":
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
