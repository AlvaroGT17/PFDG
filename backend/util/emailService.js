import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config();

const transporter = nodemailer.createTransport({
    host: process.env.EMAIL_HOST,
    port: process.env.EMAIL_PORT,
    secure: false,
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
    }
});

/**
 * Función para enviar correos electrónicos
 * @param {string} destinatario - Correo del destinatario
 * @param {string} asunto - Asunto del correo
 * @param {string} mensaje - Contenido del correo
 */
const enviarCorreo = async (destinatario, asunto, mensaje) => {
    try {
        await transporter.sendMail({
            from: process.env.EMAIL_USER,
            to: destinatario,
            subject: asunto,
            text: mensaje
        });
        console.log(`✅ Correo enviado a ${destinatario}`);
    } catch (error) {
        console.error('❌ Error al enviar el correo:', error);
        throw error;
    }
};

export default enviarCorreo;
