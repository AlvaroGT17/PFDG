"""
Inicializador para pruebas de la ventana de fichaje (`FicharControlador`).

Este módulo permite crear una instancia del controlador de fichajes con datos ficticios,
sin mostrar la interfaz. Es útil tanto para pruebas automatizadas como para integraciones
manuales durante el desarrollo.

Uso:
    Importar `iniciar_ventana_fichar()` desde otros scripts o test suites.
"""

from controladores.fichar_controlador import FicharControlador


def iniciar_ventana_fichar():
    """
    Crea un controlador de fichaje simulado con un usuario ficticio.
    No muestra la ventana, solo instancia el controlador.

    Returns:
        FicharControlador: Instancia lista para ser mostrada o utilizada en pruebas.
    """
    usuario_ficticio = {
        "id": 6,
        "nombre": "CRESNIK",
        "rol_id": 1
    }
    return FicharControlador(usuario_ficticio)
