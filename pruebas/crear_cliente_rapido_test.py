"""
Inicializador para la ventana de creación rápida de cliente.

Este módulo permite instanciar `VentanaCrearClienteRapido` sin necesidad de
una ventana principal, facilitando su uso en pruebas visuales o unitarias.

Puede emplearse para testear la validación de campos, flujos rápidos de registro
o integraciones con otros módulos.
"""

from PySide6.QtWidgets import QLineEdit
from vistas.ventana_crear_cliente_rapido import VentanaCrearClienteRapido


def iniciar_ventana_crear_cliente_rapido():
    """
    Inicializa la ventana de creación rápida de cliente sin ventana padre.

    Returns:
        VentanaCrearClienteRapido: Instancia lista para ser mostrada o usada en tests.
    """
    return VentanaCrearClienteRapido()
