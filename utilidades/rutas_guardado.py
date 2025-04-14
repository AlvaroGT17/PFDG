import os
from datetime import datetime

MESES_ESPANOL = [
    "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
    "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
]


def obtener_ruta_predeterminada_recepcionamientos():
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
