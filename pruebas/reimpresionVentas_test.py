"""
Inicializador para la ventana de reimpresión de ventas.

Este módulo permite crear una instancia de `VentanaReimpresionVentas` con datos simulados
para su uso en pruebas automatizadas u otras ejecuciones donde no se requiera interacción real.

La función devuelve la ventana con un callback vacío y valores ficticios de nombre y rol.
"""

from vistas.ventana_reimpresionVentas import VentanaReimpresionVentas


def iniciar_ventana_reimpresion_ventas():
    """
    Inicializa la ventana de reimpresión de ventas con parámetros ficticios.

    Returns:
        VentanaReimpresionVentas: Instancia configurada con datos de prueba.
    """
    return VentanaReimpresionVentas(
        nombre_usuario="PRUEBA",
        rol_usuario="Administrador",
        volver_callback=lambda: None
    )
