"""
Inicializador para el diálogo de envío de presupuestos por correo.

Este módulo proporciona una función de utilidad para crear una instancia
de `VentanaDialogoCorreoPresupuesto` sin necesidad de una ventana principal.

Es útil para pruebas visuales o unitarias donde se requiera verificar
la funcionalidad del envío de correos de presupuestos.
"""

from vistas.ventana_dialogoCorreoPresupuesto import VentanaDialogoCorreoPresupuesto


def iniciar_dialogo_correo_presupuesto():
    """
    Inicializa el diálogo de correo de presupuesto sin ventana padre.

    Returns:
        VentanaDialogoCorreoPresupuesto: Instancia lista para ser mostrada.
    """
    return VentanaDialogoCorreoPresupuesto()
