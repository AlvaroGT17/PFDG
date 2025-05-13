"""
Módulo de utilidades para el manejo de rutas absolutas dentro del proyecto.

Este módulo contiene funciones para obtener rutas absolutas a partir de rutas relativas,
garantizando compatibilidad tanto en ejecución normal como en entornos compilados (por ejemplo, con PyInstaller).

También incluye funciones para obtener las rutas predeterminadas donde se almacenarán
los documentos de compras y ventas, organizados por mes y año.
"""

import os
import sys


def obtener_ruta_absoluta(ruta_relativa: str) -> str:
    """
    Devuelve la ruta absoluta basada en la raíz del proyecto, sin importar desde dónde se llame.

    Esta función permite que cualquier recurso dentro del proyecto sea accesible
    sin depender de la ubicación actual desde la que se ejecuta el script o el binario.

    Args:
        ruta_relativa (str): Ruta relativa desde la raíz del proyecto (por ejemplo, 'img/logo.png').

    Returns:
        str: Ruta absoluta al recurso solicitado.

    Raises:
        FileNotFoundError: Si la ruta generada no existe físicamente.
    """
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable compilado (PyInstaller, por ejemplo)
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(
            __file__))  # Carpeta actual (utilidades/)

    # Subimos a la raíz del proyecto (PFDG/)
    proyecto_root = os.path.abspath(os.path.join(base_path, ".."))

    # Normalizamos la ruta relativa
    ruta_relativa = ruta_relativa.replace("\\", "/")
    ruta_absoluta = os.path.join(proyecto_root, ruta_relativa)

    if not os.path.exists(ruta_absoluta):
        raise FileNotFoundError(f"El recurso no existe: {ruta_absoluta}")

    return ruta_absoluta


def obtener_ruta_predeterminada_compras():
    """
    Genera la ruta predeterminada para almacenar documentos de compras.

    La carpeta estará ubicada dentro del proyecto en:
    'documentos/compras/NOMBRE_DEL_MES_AÑO' (por ejemplo: 'documentos/compras/MAYO_2025').

    Returns:
        str: Ruta absoluta a la carpeta correspondiente al mes actual.
    """
    from datetime import datetime
    import os
    mes_anio = datetime.now().strftime("%B_%Y").upper()
    return os.path.join("D:\\Proyecto_Final_de_Grado\\PFDG\\documentos\\compras", mes_anio)


def obtener_ruta_predeterminada_ventas():
    """
    Genera la ruta predeterminada para almacenar documentos de ventas.

    La carpeta estará ubicada dentro del proyecto en:
    'documentos/ventas/NOMBRE_DEL_MES_AÑO' (por ejemplo: 'documentos/ventas/MAYO_2025').

    Returns:
        str: Ruta absoluta a la carpeta correspondiente al mes actual.
    """
    from datetime import datetime
    import os
    mes_anio = datetime.now().strftime("%B_%Y").upper()
    return os.path.join("D:\\Proyecto_Final_de_Grado\\PFDG\\documentos\\ventas", mes_anio)
