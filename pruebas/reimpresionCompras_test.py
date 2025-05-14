from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras


def iniciar_ventana_reimpresion_compras():
    """
    Inicializa la ventana de reimpresión de compras con valores de prueba.
    """
    return VentanaReimpresionCompras(
        nombre_usuario="PRUEBA",
        rol_usuario="Administrador",
        volver_callback=lambda: None
    )
