"""
Módulo para el envío por correo electrónico de presupuestos en formato PDF.

Utiliza las credenciales definidas en un archivo `.env` para autenticarse y envía
un mensaje HTML personalizado con el archivo adjunto. Compatible con Gmail vía SMTP-SSL.
"""

import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Cargar variables de entorno (.env)
load_dotenv()


def enviar_correo_presupuesto(destinatario, ruta_pdf, datos):
    """
    Envía un correo electrónico con un presupuesto adjunto en PDF al destinatario indicado.

    El correo incluye un mensaje HTML personalizado con el logotipo y colores corporativos
    de ReyBoxes, y el archivo PDF se adjunta automáticamente.

    Args:
        destinatario (str): Dirección de correo a la que se enviará el presupuesto.
        ruta_pdf (str): Ruta absoluta al archivo PDF que se adjuntará.
        datos (dict): Diccionario de datos que debe contener al menos la clave 'cliente'
                      con el nombre del destinatario.

    Returns:
        tuple: (bool, str or None)  
            - `True` si el correo se envió correctamente.  
            - `False` y mensaje de error en caso de fallo.
    """
    remitente = os.getenv("EMAIL_USER")
    contraseña = os.getenv("EMAIL_PASS")
    nombre_cliente = datos.get("cliente", "Cliente").capitalize()

    asunto = "📄 Reenvío de presupuesto - ReyBoxes"

    # Plantilla HTML personalizada del correo
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; color: black; margin: auto; background: #f1f1f1; border-radius: 12px; padding: 20px; border: 1px solid #ccc;">
            <div style="text-align: center;">
                <img src="https://www.facebook.com/photo/?fbid=874525541341496&set=a.556411836486203&__tn__=%3C"
                alt="Logo ReyBoxes" style="max-width: 150px; border-radius: 10px; margin-bottom: 10px;" />
                <h2 style="color: #E30613; margin-bottom: 0;">Reenvío de Presupuesto</h2>
            </div>

            <p style="font-size: 16px;">
                Hola <strong style="color: #E30613;">{nombre_cliente}</strong>,
            </p>

            <p style="font-size: 16px;">
                Te reenviamos el documento del presupuesto solicitado desde 
                <strong style="color:rgb(115, 132, 150);">Rey</strong> <strong style="color: #E30613;">Boxes</strong>.
            </p>

            <p style="font-size: 16px;">
                El archivo está adjunto a este correo. Si necesitas ayuda, no dudes en escribirnos.
            </p>

            <p style="font-size: 16px;">
                ¡Gracias por contar con nosotros!
            </p>

            <hr style="border: none; border-top: 1px solid #ccc; margin: 30px 0;" />

            <p style="text-align: center; font-size: 13px; color: #999;">
                © 2025 <strong style="color:rgb(115, 132, 150);">Rey</strong> <strong style="color: #E30613;">Boxes</strong> | Mecánica y mantenimiento
            </p>
        </div>
    """

    # Crear mensaje multipart (texto + adjunto)
    mensaje = MIMEMultipart("alternative")
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(html, "html"))

    try:
        # Adjuntar el PDF
        with open(ruta_pdf, "rb") as f:
            adjunto = MIMEApplication(f.read(), _subtype="pdf")
            adjunto.add_header('Content-Disposition', 'attachment',
                               filename=os.path.basename(ruta_pdf))
            mensaje.attach(adjunto)

        # Enviar el correo por SMTP-SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)

        return True, None
    except Exception as e:
        return False, str(e)
