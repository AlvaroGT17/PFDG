from controladores.fichar_controlador import FicharControlador


def iniciar_ventana_fichar():
    """
    Crea un controlador de fichaje simulado con un usuario ficticio.
    No muestra la ventana, solo instancia el controlador.
    """
    usuario_ficticio = {
        "id": 6,
        "nombre": "CRESNIK",
        "rol_id": 1
    }
    return FicharControlador(usuario_ficticio)
