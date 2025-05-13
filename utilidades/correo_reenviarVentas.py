"""
Módulo para enviar comprobantes de venta por correo electrónico con archivo PDF adjunto.

Utiliza las credenciales definidas en un archivo `.env` para autenticarse y envía
un mensaje HTML con diseño corporativo de ReyBoxes, adjuntando el comprobante en PDF.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def enviar_correo_reimpresion_venta(destinatario, ruta_pdf):
    """
    Envía un correo electrónico con el comprobante de venta en PDF adjunto.

    El correo incluye un mensaje HTML personalizado y un archivo adjunto que contiene
    el comprobante solicitado por el cliente.

    Args:
        destinatario (str): Dirección de correo del cliente que recibirá el comprobante.
        ruta_pdf (str): Ruta absoluta al archivo PDF que se va a adjuntar.

    Returns:
        tuple:
            - bool: `True` si el correo se envió correctamente, `False` en caso de error.
            - str or None: Mensaje de error en caso de fallo, o `None` si se envió correctamente.
    """
    remitente = os.getenv("EMAIL_USER")
    contrasena = os.getenv("EMAIL_PASS")

    asunto = "📄 Comprobante de venta - ReyBoxes"

    # Cuerpo HTML del mensaje
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; color: black; margin: auto; background: #f1f1f1; border-radius: 12px; padding: 20px; border: 1px solid #ccc;">
        <div style="text-align: center;">
            <img src="https://www.facebook.com/photo/?fbid=874525541341496&set=a.556411836486203&__tn__=%3C"
            alt="Logo ReyBoxes" style="max-width: 150px; border-radius: 10px; margin-bottom: 10px;" />
            <h2 style="color: #E30613; margin-bottom: 0;">Comprobante de venta</h2>
        </div>

        <p style="font-size: 16px;">
            Adjuntamos el comprobante de venta solicitado desde <strong style="color:rgb(115, 132, 150);">Rey</strong> <strong style="color: #E30613;">Boxes</strong>.
        </p>

        <p style="font-size: 16px;">
            Revisa el archivo adjunto. Para cualquier duda o comentario, estamos a tu disposición.
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

    # Crear mensaje multipart (HTML + adjunto)
    mensaje = MIMEMultipart("alternative")
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(html, "html"))

    # Intentar adjuntar el archivo PDF
    try:
        with open(ruta_pdf, "rb") as f:
            adjunto = MIMEApplication(f.read(), _subtype="pdf")
            adjunto.add_header(
                "Content-Disposition", "attachment", filename=os.path.basename(ruta_pdf))
            mensaje.attach(adjunto)
    except Exception as e:
        return False, f"Error al adjuntar el archivo: {str(e)}"

    # Intentar enviar el correo vía SMTP-SSL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contrasena)
            servidor.send_message(mensaje)
        return True, None
    except Exception as e:
        return False, str(e)
