from vistas.ventana_reimpresionVentas import VentanaReimpresionVentas


def iniciar_ventana_reimpresion_ventas():
    """
    Inicializa la ventana de reimpresión de ventas con parámetros ficticios.
    """
    return VentanaReimpresionVentas(
        nombre_usuario="PRUEBA",
        rol_usuario="Administrador",
        volver_callback=lambda: None
    )
