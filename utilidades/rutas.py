import os
import sys


def obtener_ruta_absoluta(ruta_relativa: str) -> str:
    """
    Devuelve la ruta absoluta basada en la raíz del proyecto, sin importar desde dónde se llame.
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Si es un ejecutable compilado
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))  # utilidades/

    # Vamos a la raíz del proyecto
    proyecto_root = os.path.abspath(os.path.join(base_path, ".."))  # PFDG/

    ruta_relativa = ruta_relativa.replace("\\", "/")
    ruta_absoluta = os.path.join(proyecto_root, ruta_relativa)

    if not os.path.exists(ruta_absoluta):
        raise FileNotFoundError(f"El recurso no existe: {ruta_absoluta}")

    return ruta_absoluta
