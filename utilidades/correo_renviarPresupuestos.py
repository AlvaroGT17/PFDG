import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()


def enviar_correo_presupuesto(destinatario, ruta_pdf, datos):
    """
    Envía un presupuesto PDF al correo especificado.

    Parámetros:
    - destinatario: dirección de correo a la que se enviará
    - ruta_pdf: ruta al archivo PDF
    - datos: diccionario que debe incluir al menos 'cliente'
    """

    remitente = os.getenv("EMAIL_USER")
    contraseña = os.getenv("EMAIL_PASS")
    nombre_cliente = datos.get("cliente", "Cliente").capitalize()

    asunto = "📄 Reenvío de presupuesto - ReyBoxes"

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

    mensaje = MIMEMultipart("alternative")
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(html, "html"))

    try:
        with open(ruta_pdf, "rb") as f:
            adjunto = MIMEApplication(f.read(), _subtype="pdf")
            adjunto.add_header('Content-Disposition', 'attachment',
                               filename=os.path.basename(ruta_pdf))
            mensaje.attach(adjunto)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)

        return True, None
    except Exception as e:
        return False, str(e)
