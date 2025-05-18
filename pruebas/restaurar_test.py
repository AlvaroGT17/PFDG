"""
Inicializador para la ventana de restablecimiento de contraseña.

Este módulo expone una función `iniciar_ventana_restaurar()` que permite instanciar
la clase `VentanaRestaurar` desde el módulo de vistas sin necesidad de invocar directamente
la clase en los tests u otros controladores.

Usado comúnmente en pruebas unitarias o controladores que requieren abrir esta ventana.
"""

from vistas.ventana_restaurar import VentanaRestaurar


def iniciar_ventana_restaurar():
    """
    Inicializa la ventana de restablecimiento de contraseña.

    Returns:
        VentanaRestaurar: Instancia de la ventana correspondiente.
    """
    return VentanaRestaurar()
