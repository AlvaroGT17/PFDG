"""
Módulo de utilidades para la generación de documentos PDF de recepcionamiento.

Incluye funciones para:
- Validar correos electrónicos.
- Generar documentos PDF a partir de plantillas HTML usando Jinja2 y WeasyPrint.
- Limpiar nombres para su uso seguro como nombres de archivo.
"""

import os
import re
import unicodedata
from weasyprint import HTML
from PySide6.QtCore import QDir
from jinja2 import Environment, FileSystemLoader


def validar_correo(correo):
    """
    Valida si una cadena tiene formato de correo electrónico válido.

    Args:
        correo (str): Dirección de correo a validar.

    Returns:
        MatchObject or None: Resultado de la validación. `None` si no es válido.
    """
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", correo)


def generar_documento_pdf(datos, firma_cliente_path, ruta_guardado=None):
    """
    Genera un archivo PDF de recepcionamiento a partir de una plantilla HTML y datos proporcionados.

    Usa Jinja2 para renderizar el HTML con los datos del formulario y WeasyPrint
    para convertir ese HTML en un archivo PDF.

    Args:
        datos (dict): Diccionario con los datos a incluir en el PDF (nombre, número de recepción, etc.).
        firma_cliente_path (str): Ruta a la imagen de la firma del cliente.
        ruta_guardado (str, opcional): Carpeta donde se guardará el PDF. Si no se especifica, se crea una predeterminada.

    Returns:
        str: Ruta completa donde se ha guardado el archivo PDF generado.
    """
    import datetime
    ahora = datetime.datetime.now()
    fecha_emision = ahora.strftime("%d/%m/%Y")

    # Ruta base del proyecto
    ruta_base = QDir.currentPath()

    # Rutas a plantillas y firma del taller
    plantilla_html = os.path.join(
        ruta_base, "plantillas", "recepcionamiento.html")
    plantilla_css = os.path.join(
        ruta_base, "plantillas", "recepcionamiento.css")
    firma_taller_path = os.path.join(
        ruta_base, "plantillas", "img", "firmataller.png")

    # Preparar motor de plantillas Jinja2
    env = Environment(loader=FileSystemLoader(os.path.dirname(plantilla_html)))
    plantilla = env.get_template(os.path.basename(plantilla_html))

    # Renderizar plantilla con los datos
    html_renderizado = plantilla.render(
        datos=datos,
        firma_path=firma_cliente_path.replace("\\", "/"),
        firma_taller=firma_taller_path.replace("\\", "/"),
        fecha_emision=fecha_emision
    )

    # Generar nombre de archivo único
    nombre_cliente = limpiar_nombre_para_archivo(datos["Nombre"])
    numero_recepcion = datos.get("NúmeroRecepcion", "00000").zfill(5)
    nombre_archivo = f"Recepcion_{nombre_cliente}_{numero_recepcion}.pdf"

    # Determinar ruta de guardado
    if not ruta_guardado:
        ruta_guardado = os.path.join(
            ruta_base, "documentos", "recepcionamientos", ahora.strftime(
                "%Y-%m")
        )
    os.makedirs(ruta_guardado, exist_ok=True)
    ruta_pdf = os.path.join(ruta_guardado, nombre_archivo)

    # Generar PDF desde HTML renderizado
    HTML(string=html_renderizado, base_url=ruta_base).write_pdf(
        ruta_pdf,
        stylesheets=[plantilla_css]
    )

    return ruta_pdf


def limpiar_nombre_para_archivo(nombre):
    """
    Limpia y formatea una cadena para que pueda ser usada como nombre de archivo válido.

    Reemplaza caracteres especiales por guiones bajos y convierte a mayúsculas.

    Args:
        nombre (str): Nombre original del cliente o entidad.

    Returns:
        str: Nombre limpio, adecuado para ser usado como nombre de archivo.
    """
    nombre = nombre.upper()
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = nombre.encode('ascii', 'ignore').decode("utf-8")
    nombre = re.sub(r'[^A-Z0-9_]', '_', nombre)
    return nombre
