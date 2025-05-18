"""
Inicializador para la ventana de reimpresión de presupuestos.

Este módulo proporciona una función de utilidad para instanciar la clase
`VentanaReimpresionPresupuestos` con parámetros ficticios, facilitando su uso
en pruebas automatizadas o scripts de testeo visual.

La instancia generada no depende del estado de la aplicación principal.
"""

from vistas.ventana_reimpresionPresupuestos import VentanaReimpresionPresupuestos


def iniciar_ventana_reimpresion_presupuestos():
    """
    Inicializa la ventana de reimpresión de presupuestos con valores ficticios.

    Returns:
        VentanaReimpresionPresupuestos: Instancia preparada para pruebas.
    """
    return VentanaReimpresionPresupuestos(
        nombre_usuario="PRUEBA",
        rol_usuario="Administrador",
        volver_callback=lambda: None
    )
