import re
import tempfile
from datetime import datetime

# Puedes usar reportlab o fpdf, dependiendo de tus preferencias.
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def validar_correo(correo):
    """
    Valida el formato de un correo electrónico.
    """
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None


def capturar_firma():
    """
    Captura la firma del cliente desde una tableta digitalizadora.

    IMPORTANTE: Esta función solo debe devolver la imagen temporalmente en memoria
    para ser usada al momento de estamparla. No se debe guardar en base de datos.

    Retorna:
        QImage o ruta temporal del archivo PNG de la firma.
    """
    # TODO: Integrar con tableta digitalizadora real.
    # Por ahora dejamos un marcador de posición.
    print("⚠️ Función de captura de firma aún no implementada.")
    return None


def generar_documento_pdf(datos, firma_img=None):
    """
    Genera un documento PDF del recepcionamiento con los datos y la firma.

    Args:
        datos (dict): Diccionario con los datos del formulario.
        firma_img (QImage o ruta): Firma digital capturada, opcional.

    Retorna:
        str: Ruta temporal del archivo PDF generado.
    """
    ruta_temp = tempfile.mktemp(suffix=".pdf")
    c = canvas.Canvas(ruta_temp, pagesize=A4)
    ancho, alto = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, alto - 50, "Recepcionamiento de Vehículo")

    c.setFont("Helvetica", 10)
    y = alto - 80
    for clave, valor in datos.items():
        if valor is not None:
            c.drawString(50, y, f"{clave}: {valor}")
            y -= 15

    if firma_img:
        # TODO: estampar firma en el PDF (cuando se tenga la imagen en archivo o QImage)
        c.drawString(50, y - 20, "[Firma capturada]")

    c.save()
    return ruta_temp
