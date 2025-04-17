import os
import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from PySide6.QtCore import QDir
import unicodedata
import re


def validar_correo(correo):
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", correo)


def generar_documento_pdf(datos, firma_cliente_path, ruta_guardado=None):
    import datetime
    ahora = datetime.datetime.now()  # ✅ Se define correctamente aquí
    fecha_emision = ahora.strftime("%d/%m/%Y")  # ✅ Formato DD/MM/YYYY

    # Ruta base del proyecto
    ruta_base = QDir.currentPath()

    # Rutas absolutas a plantilla HTML, CSS y firma del taller
    plantilla_html = os.path.join(
        ruta_base, "plantillas", "recepcionamiento.html")
    plantilla_css = os.path.join(
        ruta_base, "plantillas", "recepcionamiento.css")
    firma_taller_path = os.path.join(
        ruta_base, "plantillas", "img", "firmataller.png")

    # Preparar entorno de Jinja2 con la carpeta de plantillas
    env = Environment(loader=FileSystemLoader(os.path.dirname(plantilla_html)))
    plantilla = env.get_template(os.path.basename(plantilla_html))

    # Rellenar HTML con datos
    html_renderizado = plantilla.render(
        datos=datos,
        firma_path=firma_cliente_path.replace("\\", "/"),
        firma_taller=firma_taller_path.replace("\\", "/"),
        fecha_emision=fecha_emision  # ✅ Se pasa a la plantilla
    )

    # Generar nombre de archivo único
    nombre_cliente = limpiar_nombre_para_archivo(datos["Nombre"])
    numero_recepcion = datos.get("NúmeroRecepcion", "00000").zfill(5)
    nombre_archivo = f"Recepcion_{nombre_cliente}_{numero_recepcion}.pdf"

    # Ruta de guardado
    if not ruta_guardado:
        ruta_guardado = os.path.join(
            ruta_base, "documentos", "recepcionamientos", ahora.strftime(
                "%Y-%m")
        )
    os.makedirs(ruta_guardado, exist_ok=True)
    ruta_pdf = os.path.join(ruta_guardado, nombre_archivo)

    # Generar el PDF
    HTML(string=html_renderizado, base_url=ruta_base).write_pdf(
        ruta_pdf,
        stylesheets=[plantilla_css]
    )

    return ruta_pdf


def limpiar_nombre_para_archivo(nombre):
    nombre = nombre.upper()
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = nombre.encode('ascii', 'ignore').decode("utf-8")
    nombre = re.sub(r'[^A-Z0-9_]', '_', nombre)
    return nombre
