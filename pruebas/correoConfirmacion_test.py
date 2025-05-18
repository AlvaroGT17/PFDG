"""
Inicializador para la ventana de confirmación de correo.

Este módulo permite crear una instancia de `VentanaCorreoConfirmacion`
con un correo de prueba predefinido. Es útil para pruebas visuales o unitarias
relacionadas con la visualización y validación del correo antes del envío.

Puede integrarse fácilmente en flujos de testeo manual o automatizado.
"""

from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion


def iniciar_ventana_correo_confirmacion():
    """
    Crea una instancia de la ventana de confirmación de correo con un correo de ejemplo.

    Returns:
        VentanaCorreoConfirmacion: Instancia lista para ser mostrada o usada en pruebas.
    """
    correo_defecto = "cliente@ejemplo.com"
    return VentanaCorreoConfirmacion(correo_defecto)
