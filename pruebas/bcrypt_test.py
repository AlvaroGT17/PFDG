"""
Módulo de utilidades para encriptación y verificación de contraseñas usando `bcrypt`.

Incluye funciones para:
- Generar un hash seguro de una contraseña en texto plano.
- Verificar si una contraseña coincide con su hash.

Este módulo también puede ejecutarse directamente desde consola para realizar
una prueba interactiva básica.

Forma parte del sistema de autenticación del proyecto ReyBoxes.
"""

import bcrypt


def encriptar_contrasena(contrasena_plana: str) -> str:
    """
    Genera un hash bcrypt seguro a partir de una contraseña en texto plano.

    Args:
        contrasena_plana (str): Contraseña sin cifrar introducida por el usuario.

    Returns:
        str: Contraseña cifrada (hash) en formato UTF-8.
    """
    hashed = bcrypt.hashpw(contrasena_plana.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con un hash bcrypt almacenado.

    Args:
        contrasena_plana (str): Contraseña sin cifrar introducida por el usuario.
        contrasena_hash (str): Hash previamente generado y almacenado.

    Returns:
        bool: `True` si la contraseña coincide, `False` en caso contrario.
    """
    return bcrypt.checkpw(contrasena_plana.encode("utf-8"), contrasena_hash.encode("utf-8"))


if __name__ == "__main__":
    """
    Prueba interactiva para verificar el funcionamiento de cifrado y verificación.

    Permite al usuario:
    - Introducir una contraseña.
    - Ver el hash generado.
    - Confirmar si una segunda entrada coincide con el hash.
    """
    print("🧪 Prueba de encriptación y verificación de contraseña con bcrypt")

    contrasena = input("🔐 Introduce una contraseña a cifrar: ")
    hash_generado = encriptar_contrasena(contrasena)

    print(f"\n📝 Hash generado:\n{hash_generado}\n")

    intento = input("👤 Introduce la contraseña nuevamente para verificar: ")

    if verificar_contrasena(intento, hash_generado):
        print("✅ Contraseña correcta")
    else:
        print("❌ Contraseña incorrecta")
