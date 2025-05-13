"""
Módulo para enviar contratos de compra o venta de vehículos por correo electrónico con PDF adjunto.

El correo incluye un diseño visual adaptado a la estética de ReyBoxes. 
Se personaliza el tipo de contrato (compra o venta), el asunto y el saludo con el nombre del cliente.
Las credenciales del remitente se obtienen desde un archivo `.env`.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Cargar variables de entorno (EMAIL_USER, EMAIL_PASS)
load_dotenv()


def enviar_correo_contrato(destinatario, ruta_pdf, datos, tipo="compra"):
    """
    Envía un correo electrónico con el contrato de compra o venta en formato PDF adjunto.

    El mensaje contiene un diseño HTML con el logotipo y colores corporativos de ReyBoxes,
    adaptando el contenido según el tipo de operación ('compra' o 'venta').

    Args:
        destinatario (str): Dirección de correo electrónico del cliente.
        ruta_pdf (str): Ruta absoluta al archivo PDF generado.
        datos (dict): Diccionario con al menos la clave 'Nombre' para personalizar el saludo.
        tipo (str, opcional): Tipo de contrato. Puede ser 'compra' o 'venta'. Por defecto es 'compra'.

    Returns:
        tuple:
            - bool: `True` si el correo fue enviado correctamente, `False` si hubo un error.
            - str or None: Mensaje de error en caso de fallo, o `None` si fue exitoso.
    """
    remitente = os.getenv("EMAIL_USER")
    contraseña = os.getenv("EMAIL_PASS")
    nombre_cliente = datos["Nombre"].strip().capitalize()
    tipo_mayus = tipo.upper()

    asunto = f"📄 Contrato de {tipo_mayus} de vehículo - ReyBoxes"

    # Plantilla HTML del mensaje
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; color: black; margin: auto; background: #f1f1f1; border-radius: 12px; padding: 20px; border: 1px solid #ccc;">
            <div style="text-align: center;">
                <img src="https://www.facebook.com/photo/?fbid=874525541341496&set=a.556411836486203&__tn__=%3C"
                alt="Logo ReyBoxes" style="max-width: 150px; border-radius: 10px; margin-bottom: 10px;" />
                <h2 style="color: #E30613; margin-bottom: 0;">Contrato de {tipo_mayus}</h2>
            </div>

            <p style="font-size: 16px;">
                Hola <strong style="color: #E30613;">{nombre_cliente}</strong>,
            </p>

            <p style="font-size: 16px;">
                Te enviamos adjunto el contrato correspondiente a la <strong>{tipo_mayus}</strong> de tu vehículo realizada con
                <strong style="color:rgb(115, 132, 150);">Rey</strong> <strong style="color: #E30613;">Boxes</strong>.
            </p>

            <p style="font-size: 16px;">
                Revisa el documento adjunto y no dudes en contactarnos si tienes alguna consulta.
            </p>

            <p style="font-size: 16px;">
                ¡Gracias por confiar en nosotros!
            </p>

            <hr style="border: none; border-top: 1px solid #ccc; margin: 30px 0;" />

            <p style="text-align: center; font-size: 13px; color: #999;">
                © 2025 <strong style="color:rgb(115, 132, 150);">Rey</strong> <strong style="color: #E30613;">Boxes</strong> | Mecánica y mantenimiento
            </p>
        </div>
    """

    # Crear mensaje MIME (HTML + adjunto)
    mensaje = MIMEMultipart("alternative")
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(html, "html"))

    # Adjuntar el PDF
    with open(ruta_pdf, "rb") as f:
        pdf_adjunto = MIMEApplication(f.read(), _subtype="pdf")
        pdf_adjunto.add_header(
            'Content-Disposition', 'attachment', filename=os.path.basename(ruta_pdf))
        mensaje.attach(pdf_adjunto)

    # Enviar el correo usando SMTP con SSL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
        return True, None
    except Exception as e:
        return False, str(e)
