import psycopg2
from psycopg2 import sql
from datetime import datetime
import bcrypt
# Asegúrate de tener esta función
from modelos.conexion_bd import obtener_conexion


def obtener_roles():
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
