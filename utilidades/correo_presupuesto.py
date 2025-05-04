import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()


def enviar_correo_presupuesto(destinatario, ruta_pdf, datos):
    """
    Envía por correo el PDF del presupuesto al cliente.

    Parámetros:
    - destinatario: correo electrónico del cliente
    - ruta_pdf: ruta al PDF generado
    - datos: diccionario con al menos las claves:
        - 'cliente': nombre del cliente
    """

    remitente = os.getenv("EMAIL_USER")
    contraseña = os.getenv("EMAIL_PASS")
    nombre_cliente = datos.get("cliente", "").strip().capitalize()

    asunto = "📄 Presupuesto de reparación - ReyBoxes"

    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; color: black; margin: auto; background: #f1f1f1; border-radius: 12px; padding: 20px; border: 1px solid #ccc;">
            <div style="text-align: center;">
                <img src="https://www.facebook.com/photo/?fbid=874525541341496&set=a.556411836486203&__tn__=%3C"
                alt="Logo ReyBoxes" style="max-width: 150px; border-radius: 10px; margin-bottom: 10px;" />
                <h2 style="color: #E30613; margin-bottom: 0;">Presupuesto de Reparación</h2>
            </div>

            <p style="font-size: 16px;">
                Hola <strong style="color: #E30613;">{nombre_cliente}</strong>,
            </p>

            <p style="font-size: 16px;">
                Te enviamos adjunto el presupuesto de reparación correspondiente a tu vehículo registrado en 
                <strong style="color:rgb(115, 132, 150);">Rey</strong> <strong style="color: #E30613;">Boxes</strong>.
            </p>

            <p style="font-size: 16px;">
                Revisa el documento adjunto y no dudes en contactarnos si tienes alguna consulta o deseas confirmar la intervención.
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

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
        return True, None
    except Exception as e:
        return False, str(e)
