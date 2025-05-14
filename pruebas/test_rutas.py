"""
Tests automáticos para funciones de utilidad relacionadas con rutas absolutas.

Este test comprueba que se puede localizar correctamente el archivo
'css/verificar_codigo.css' utilizando la función `obtener_ruta_absoluta`.

Esto asegura que el archivo existe y que la función construye rutas válidas
según la estructura del proyecto, independientemente del directorio actual.
"""

import pytest
from utilidades.rutas import obtener_ruta_absoluta
import os


def test_ruta_css_verificar_codigo():
    """
    Verifica que la ruta al archivo CSS de verificación existe y es accesible.
    """
    ruta = obtener_ruta_absoluta("css/verificar_codigo.css")
    assert os.path.exists(ruta), f"El archivo no se encuentra en: {ruta}"
