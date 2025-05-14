from vistas.ventana_reimpresionPresupuestos import VentanaReimpresionPresupuestos


def iniciar_ventana_reimpresion_presupuestos():
    """
    Inicializa la ventana de reimpresión de presupuestos con valores ficticios.
    """
    return VentanaReimpresionPresupuestos(
        nombre_usuario="PRUEBA",
        rol_usuario="Administrador",
        volver_callback=lambda: None
    )
