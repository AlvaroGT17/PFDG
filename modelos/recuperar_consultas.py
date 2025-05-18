"""
Módulo para la recuperación de cuentas mediante el envío de códigos por correo electrónico.

Este módulo permite:
- Verificar si un usuario existe mediante su email.
- Generar y guardar un código de recuperación temporal con expiración.
- Enviar un correo HTML con el código de recuperación personalizado.

Requiere conexión a una base de datos PostgreSQL y configuración de variables
de entorno para el correo emisor y las credenciales de la base de datos.
"""
import os
import random
import smtplib
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utilidades.rutas import obtener_ruta_absoluta


load_dotenv()


def enviar_codigo_recuperacion(correo_usuario):
    """
    Envía un código de recuperación de cuenta al correo del usuario.

    - Verifica si el correo está registrado en la tabla `usuarios`.
    - Genera un código numérico de 6 cifras válido por 5 minutos.
    - Guarda el código y su fecha de expiración en la base de datos.
    - Envía un correo electrónico con el código utilizando formato HTML.

    Args:
        correo_usuario (str): Dirección de correo del usuario que solicita la recuperación.

    Returns:
        bool: True si el código fue generado y enviado correctamente, False si hubo un error o el correo no existe.
    """
    conexion = None
    try:
        # 1. Conexión a la base de datos
        conexion = psycopg2.connect(
            dbname=os.getenv("DB_NOMBRE"),
            user=os.getenv("DB_USUARIO"),
            password=os.getenv("DB_CONTRASENA"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PUERTO"),
            sslmode="require"
        )
        cursor = conexion.cursor()

        # 2. Verificar existencia del usuario
        cursor.execute(
            "SELECT id, nombre FROM usuarios WHERE email = %s", (correo_usuario,))
        resultado = cursor.fetchone()

        if not resultado:
            print("❌ No se encontró el usuario con ese correo.")
            return False

        usuario_id, nombre = resultado
        codigo = str(random.randint(100000, 999999))
        expiracion = datetime.utcnow() + timedelta(minutes=5)

        # 3. Guardar código y expiración
        cursor.execute("""
            UPDATE usuarios
            SET codigo_recuperacion = %s, expiracion_codigo = %s
            WHERE id = %s
        """, (codigo, expiracion, usuario_id))
        conexion.commit()

        # 4. Enviar correo HTML
        enviar_correo(nombre, correo_usuario, codigo)

        print(f"📧 Código enviado correctamente a {correo_usuario}")
        return True

    except Exception as e:
        print("❌ Error al enviar código:", e)
        return False

    finally:
        if conexion:
            cursor.close()
            conexion.close()


def enviar_correo(nombre, destinatario, codigo):
    """
    Envía un correo HTML con el código de recuperación al usuario.

    El mensaje contiene estilo personalizado, branding de ReyBoxes,
    y una advertencia de expiración del código.

    Args:
        nombre (str): Nombre del destinatario (formateado en el cuerpo del mensaje).
        destinatario (str): Dirección de correo electrónico del destinatario.
        codigo (str): Código de recuperación generado.

    Variables de entorno requeridas:
        - CORREO_REMITENTE: Dirección de email configurada como remitente.
        - CORREO_CONTRASENA: Contraseña o clave de aplicación del correo emisor.
    """
    nombre_formateado = nombre.strip().capitalize()
    asunto = "🔐 Recuperación de cuenta - 🚗ReyBoxes"

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; color: black; margin: auto; background: #f1f1f1; border-radius: 12px; padding: 20px; border: 1px solid #ccc;">
        <div style="text-align: center;">
            <img src="https://scontent-mad1-1.xx.fbcdn.net/v/t39.30808-1/415751285_874525538008163_7351325140883369283_n.jpg?stp=dst-jpg_s200x200_tt6&_nc_cat=106&ccb=1-7&_nc_sid=2d3e12&_nc_ohc=Q_wgsHHpx2sQ7kNvgGK1c_B&_nc_oc=AdmyZBDIRwkBZpknf5Gzm834ojdZhh8Wn7jllEnHZ7cgNlFUNweEbfZocAaXC33Troc5QQdWWkzwSLDNjAfAhVtb&_nc_zt=24&_nc_ht=scontent-mad1-1.xx&_nc_gid=ysM0cfODDM8xcSfUO8ZX6w&oh=00_AYHmaswlJ02hb0OFRK88L91llLgyKubQOrVGM5QLgduWHg&oe=67E30EBC"
                alt="Logo ReyBoxes"
                style="max-width: 150px; border-radius: 10px; margin-bottom: 10px;" />
            <h2 style="color: #E30613; margin-bottom: 0;">Código de recuperación</h2>
        </div>

        <p style="font-size: 16px; color: black;">
            Hola, <strong style="color: #E30613;">{nombre_formateado}</strong>,
        </p>

        <p style="font-size: 16px; color: black;">
            Recibimos una solicitud para restablecer tu contraseña en <strong style="color:rgb(115, 132, 150);">Rey</strong> <strong style="color: #E30613;">Boxes</strong>.
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

    remitente = os.getenv("CORREO_REMITENTE")
    contrasena = os.getenv("CORREO_CONTRASENA")

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remitente, contrasena)
        servidor.send_message(mensaje)
