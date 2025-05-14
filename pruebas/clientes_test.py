# pruebas/clientes_test.py
from vistas.ventana_clientes import VentanaClientes


def iniciar_ventana_clientes():
    """Inicializa la ventana de gestión de clientes sin ventana padre."""
    return VentanaClientes(None)
