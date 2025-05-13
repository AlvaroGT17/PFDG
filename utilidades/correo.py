"""
Módulo de utilidades para el envío de correos electrónicos con códigos de recuperación de cuenta.

Utiliza el protocolo SMTP con SSL para enviar un mensaje personalizado al usuario con
su código de verificación. La plantilla HTML está diseñada con los estilos visuales de ReyBoxes.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


def enviar_correo(destinatario, nombre_usuario, codigo):
    """
    Envía un correo electrónico con un código de recuperación de cuenta a un destinatario específico.

    El mensaje incluye una plantilla HTML personalizada con el estilo corporativo de ReyBoxes.
    Utiliza credenciales definidas en variables de entorno (.env) para autenticar el envío.

    Args:
        destinatario (str): Dirección de correo del destinatario.
        nombre_usuario (str): Nombre del usuario que recibirá el código (se normaliza).
        codigo (str): Código de recuperación temporal que se enviará por correo.

    Raises:
        Exception: Propaga cualquier error relacionado con la conexión o envío del correo.
    """
    # Normalizar nombre para mostrar con la primera letra mayúscula
    nombre_normalizado = nombre_usuario.strip().capitalize()

    # Configuración del remitente (desde .env)
    remitente = os.getenv("EMAIL_USER")
    contraseña = os.getenv("EMAIL_PASS")
    asunto = "🔐 Recuperación de cuenta - 🚗 ReyBoxes"

    # Cuerpo HTML del mensaje
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; color: black; margin: auto; background: #f1f1f1; border-radius: 12px; padding: 20px; border: 1px solid #ccc;">
            <div style="text-align: center;">
                <img src="https://scontent-mad1-1.xx.fbcdn.net/v/t39.30808-6/415751285_874525538008163_7351325140883369283_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=gUw4mD02ckEQ7kNvgH3L28l&_nc_oc=AdmXIuxkTubdFB4r5ade3UMMMH9Nl8WlDJppLUmqIlhbaS5VLmJvdwbgnNBTMaoWWPdGXx-t16sw04TFPUE-5g1O&_nc_zt=23&_nc_ht=scontent-mad1-1.xx&_nc_gid=hf3BWj-cnV-OFf4f-kIKIQ&oh=00_AYEWAHl6_bh33YPUNsWKf372IpfTdQ5xXm9-icVOzGjfJQ&oe=67ECB23E"
                alt="Logo ReyBoxes" style="max-width: 150px; border-radius: 10px; margin-bottom: 10px;" />
                <h2 style="color: #E30613; margin-bottom: 0;">Código de recuperación</h2>
            </div>

            <p style="font-size: 16px; color: black;">
                Hola, <strong style="color: #E30613;">{nombre_normalizado}</strong>,
            </p>

            <p style="font-size: 16px; color: black;">
                Recibimos una solicitud para restablecer tu contraseña en 
                <strong style="color:rgb(115, 132, 150);">Rey</strong> 
                <strong style="color: #E30613;">Boxes</strong>.
                Usa el siguiente código para continuar con el proceso:
            </p>

            <div style="text-align: center; margin: 20px 0;">
                <span style="display: inline-block; font-size: 24px; font-weight: bold; color: #FFC107; border: 2px dashed #E30613; padding: 10px 30px; border-radius: 8px;">
                    {codigo}
                </span>
            </div>

            <p style="font-size: 16px; color: black;">
                Este código expirará en <strong>5 minutos</strong>.
            </p>

            <p style="font-size: 16px; color: black;">
                Si no solicitaste este código, simplemente ignora este mensaje. Tu cuenta sigue segura.
            </p>

            <hr style="border: none; border-top: 1px solid #ccc; margin: 30px 0;" />

            <p style="text-align: center; font-size: 13px; color: #999;">
                © 2025 <strong style="color:rgb(115, 132, 150);">Rey</strong> <strong style="color: #E30613;">Boxes</strong> | Mecánica y mantenimiento
            </p>
        </div>
    """

    # Configurar el mensaje MIME
    mensaje = MIMEMultipart("alternative")
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(html, "html"))

    # Enviar el correo por SMTP con SSL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, contraseña)
            servidor.send_message(mensaje)
            print("📨 Correo enviado correctamente a", destinatario)
    except Exception as e:
        print("❌ Error al enviar correo:", e)
        raise
