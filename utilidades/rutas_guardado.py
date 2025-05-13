"""
Módulo de utilidades para generar la ruta predeterminada de almacenamiento de recepcionamientos.

Este módulo calcula la carpeta de destino para los documentos generados en recepcionamientos,
creando automáticamente una carpeta con el formato 'MES_AÑO' en español.
"""

import os
from datetime import datetime

# Lista con los nombres de los meses en español, en mayúsculas
MESES_ESPANOL = [
    "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
    "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
]


def obtener_ruta_predeterminada_recepcionamientos():
    """
    Genera y devuelve la ruta absoluta donde se guardarán los documentos
    de recepcionamientos, organizados por mes y año en español.

    La ruta se construye automáticamente en la carpeta:
    'documentos/recepcionamientos/MES_AÑO', por ejemplo:
    'documentos/recepcionamientos/ABRIL_2025'.

    Si la carpeta no existe, se crea automáticamente.

    Returns:
        str: Ruta absoluta a la carpeta de recepcionamientos correspondiente al mes actual.
    """
    # Ruta base donde está instalado el programa
    ruta_base = os.path.dirname(os.path.abspath(__file__))

    # Nombre del mes actual en español
    mes_actual = MESES_ESPANOL[datetime.now().month - 1]
    anio_actual = str(datetime.now().year)

    # Carpeta final tipo documentos/recepcionamientos/ABRIL_2025
    ruta_destino = os.path.join(
        ruta_base, "..", "documentos", "recepcionamientos", f"{mes_actual}_{anio_actual}")
    ruta_destino = os.path.abspath(ruta_destino)

    # Crear carpeta si no existe
    os.makedirs(ruta_destino, exist_ok=True)

    return ruta_destino
