"""
Módulo de utilidad para convertir archivos HTML en documentos PDF.

Utiliza la librería WeasyPrint para realizar la conversión y guardar el resultado
en una ubicación específica del sistema de archivos.
"""

import os
from weasyprint import HTML


def convertir_html_a_pdf(ruta_html, carpeta_destino, nombre_archivo_pdf):
    """
    Convierte un archivo HTML a PDF y lo guarda en la carpeta especificada.

    Esta función utiliza la librería WeasyPrint para transformar un documento HTML
    en un archivo PDF. Si la carpeta de destino no existe, se crea automáticamente.
    Devuelve la ruta del archivo generado si el proceso fue exitoso.

    Args:
        ruta_html (str): Ruta al archivo HTML de origen (puede ser una ruta local o URL).
        carpeta_destino (str): Carpeta donde se guardará el PDF generado.
        nombre_archivo_pdf (str): Nombre que se le dará al archivo PDF (debe incluir '.pdf').

    Returns:
        str or None: Ruta completa al PDF generado si tuvo éxito, o None si ocurrió un error.
    """
    try:
        os.makedirs(carpeta_destino, exist_ok=True)
        ruta_pdf = os.path.join(carpeta_destino, nombre_archivo_pdf)
        HTML(ruta_html).write_pdf(ruta_pdf)
        return ruta_pdf
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        return None
