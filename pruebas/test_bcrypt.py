"""
Módulo de utilidades de encriptación de contraseñas usando bcrypt.

Contiene funciones para generar hashes seguros y para verificar contraseñas.
Las pruebas se centran exclusivamente en validar el correcto comportamiento
de estas funciones internas del proyecto, sin testear la biblioteca bcrypt en sí.

Funciones:
    - encriptar_contrasena: genera un hash seguro a partir de una contraseña plana.
    - verificar_contrasena: compara una contraseña con su hash bcrypt.

"""

import bcrypt


def encriptar_contrasena(contrasena_plana: str) -> str:
    """
    Genera un hash seguro (bcrypt) a partir de una contraseña en texto plano.

    Args:
        contrasena_plana (str): La contraseña original sin cifrar.

    Returns:
        str: La contraseña encriptada como hash bcrypt.
    """
    hashed = bcrypt.hashpw(contrasena_plana.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash bcrypt.

    Args:
        contrasena_plana (str): Contraseña sin cifrar.
        contrasena_hash (str): Hash previamente generado con bcrypt.

    Returns:
        bool: True si coinciden, False en caso contrario.
    """
    return bcrypt.checkpw(contrasena_plana.encode("utf-8"), contrasena_hash.encode("utf-8"))


# ---------------------------- TESTS ÚTILES PARA EL PROYECTO ---------------------------- #

def test_encriptar_contrasena_genera_hash_distinto():
    """
    Verifica que el hash generado sea distinto de la contraseña original
    y tenga un formato válido de bcrypt.
    """
    contrasena = "MiContraseñaSegura123"
    hash_resultado = encriptar_contrasena(contrasena)

    assert hash_resultado != contrasena
    assert isinstance(hash_resultado, str)
    assert hash_resultado.startswith("$2")  # Formato estándar de bcrypt


def test_verificar_contrasena_correcta():
    """
    Verifica que una contraseña cifrada sea correctamente verificada.
    """
    contrasena = "ReyBoxes2025"
    hash_generado = encriptar_contrasena(contrasena)

    assert verificar_contrasena(contrasena, hash_generado) is True


def test_verificar_contrasena_incorrecta():
    """
    Verifica que una contraseña incorrecta no pase la validación contra un hash.
    """
    contrasena = "ClaveOriginal"
    hash_generado = encriptar_contrasena(contrasena)

    assert verificar_contrasena("ClaveFalsa", hash_generado) is False
