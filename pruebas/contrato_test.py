"""
Inicializador para la ventana de contrato (`VentanaContrato`) con HTML simulado.

Este módulo crea un archivo HTML temporal con contenido básico de contrato
y lo carga en una instancia de `VentanaContrato`. Es útil para pruebas visuales
de la interfaz o tests automáticos que no dependan de datos reales.

El archivo `contrato_test_temp.html` se crea solo si no existe.
"""

from vistas.ventana_contrato import VentanaContrato
from utilidades.rutas import obtener_ruta_absoluta
import os


def iniciar_ventana_contrato():
    """
    Inicializa la ventana de contrato con un archivo HTML de prueba.

    Returns:
        VentanaContrato: Instancia lista para mostrarse con contenido simulado.
    """
    # Usamos un archivo temporal de prueba con HTML básico
    ruta_html = os.path.join(os.path.dirname(
        __file__), "contrato_test_temp.html")

    if not os.path.exists(ruta_html):
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(
                "<html><body><h1>Contrato de prueba</h1><p>Contenido simulado.</p></body></html>")

    return VentanaContrato(ruta_html, "compra")
