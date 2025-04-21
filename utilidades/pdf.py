import os
from weasyprint import HTML


def convertir_html_a_pdf(ruta_html, carpeta_destino, nombre_archivo_pdf):
    """
    Convierte un archivo HTML a PDF y lo guarda en la ruta indicada.
    Devuelve la ruta del archivo PDF si tuvo éxito, o None si falló.
    """
    try:
        os.makedirs(carpeta_destino, exist_ok=True)
        ruta_pdf = os.path.join(carpeta_destino, nombre_archivo_pdf)
        HTML(ruta_html).write_pdf(ruta_pdf)
        return ruta_pdf
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        return None
