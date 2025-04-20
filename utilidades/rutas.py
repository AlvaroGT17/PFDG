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


def obtener_ruta_predeterminada_compras():
    from datetime import datetime
    import os
    mes_anio = datetime.now().strftime("%B_%Y").upper()
    return os.path.join("D:\\Proyecto_Final_de_Grado\\PFDG\\documentos\\compras", mes_anio)


def obtener_ruta_predeterminada_ventas():
    from datetime import datetime
    import os
    mes_anio = datetime.now().strftime("%B_%Y").upper()
    return os.path.join("D:\\Proyecto_Final_de_Grado\\PFDG\\documentos\\ventas", mes_anio)
