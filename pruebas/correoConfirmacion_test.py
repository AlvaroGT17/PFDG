from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion


def iniciar_ventana_correo_confirmacion():
    """
    Crea una instancia de la ventana de confirmación de correo con un correo de ejemplo.
    """
    correo_defecto = "cliente@ejemplo.com"
    return VentanaCorreoConfirmacion(correo_defecto)
