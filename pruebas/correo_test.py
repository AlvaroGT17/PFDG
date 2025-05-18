"""
Script de prueba para el envío de correos de recuperación.

Este módulo proporciona una función para llamar a `enviar_correo` con datos simulados,
permitiendo validar que la función de correo funciona correctamente durante el desarrollo
o pruebas controladas.

Puede usarse directamente o importarse desde `test_correo.py`.
"""

from utilidades.correo import enviar_correo


def probar_envio_correo():
    """
    Llama a la función enviar_correo con datos simulados.

    Se usa normalmente en `test_correo.py` o desde scripts manuales
    para comprobar que el envío se realiza correctamente.

    Returns:
        None
    """
    nombre = "CRESNIK"
    correo = "cresnik17021983@gmail.com"
    codigo = "123456"
    enviar_correo(correo, nombre, codigo)
