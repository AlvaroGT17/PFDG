from PySide6.QtWidgets import QLineEdit
from vistas.ventana_crear_cliente_rapido import VentanaCrearClienteRapido


def iniciar_ventana_crear_cliente_rapido():
    """Inicializa la ventana de creación rápida de cliente sin ventana padre."""
    return VentanaCrearClienteRapido()
