"""
Inicializador para la ventana de recuperación de cuenta.

Este módulo proporciona una función de utilidad para instanciar `VentanaRecuperar`
de forma sencilla, sin necesidad de invocar directamente la clase desde
otras partes del sistema.

Es útil para pruebas unitarias, tests visuales o controladores que requieran
mostrar la ventana sin depender del flujo completo de la aplicación.
"""

from vistas.ventana_recuperar import VentanaRecuperar


def iniciar_ventana_recuperar():
    """
    Crea una instancia de la ventana de recuperación de cuenta.

    Returns:
        VentanaRecuperar: Instancia de la ventana correspondiente.
    """
    return VentanaRecuperar()
