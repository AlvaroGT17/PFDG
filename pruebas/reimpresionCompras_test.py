"""
Inicializador para la ventana de reimpresión de compras.

Este módulo permite crear una instancia de `VentanaReimpresionCompras` con parámetros
de prueba, útil para realizar tests visuales o funcionales de manera aislada,
sin necesidad de ejecutar la aplicación completa.

Ideal para desarrolladores que desean verificar el comportamiento o diseño
de esta pantalla de forma independiente.
"""

from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras


def iniciar_ventana_reimpresion_compras():
    """
    Inicializa la ventana de reimpresión de compras con valores de prueba.

    Returns:
        VentanaReimpresionCompras: Instancia configurada con datos ficticios.
    """
    return VentanaReimpresionCompras(
        nombre_usuario="PRUEBA",
        rol_usuario="Administrador",
        volver_callback=lambda: None
    )
