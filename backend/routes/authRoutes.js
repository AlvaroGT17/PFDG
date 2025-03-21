import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import Usuario from '../models/Usuario.js';
import dotenv from 'dotenv';
import nodemailer from 'nodemailer';
import enviarCorreo from '../util/emailService.js';
import moment from 'moment';
import { literal } from 'sequelize';

dotenv.config();
const router = express.Router();

// Ruta para manejar el login
router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        const usuario = await Usuario.findOne({ where: { email } });

        if (!usuario) {
            return res.status(404).json({ message: 'Usuario no encontrado' });
        }

        //console.log("💡 Contraseña ingresada por el usuario:", password);
        //console.log("🔒 Contraseña almacenada en BD:", usuario.password);

        // Comparar contraseña con bcrypt
        const validPassword = await bcrypt.compare(password, usuario.password);

        if (!validPassword) {
            console.log("❌ Las contraseñas NO coinciden");
            return res.status(401).json({ message: 'Contraseña incorrecta' });
        }

        console.log("✅ Contraseña correcta, generando token...");
        const token = jwt.sign(
            { id: usuario.id, email: usuario.email, rol: usuario.rol },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );

        res.json({ token, usuario: { id: usuario.id, nombre: usuario.nombre, apellido: usuario.apellido, email: usuario.email, rol: usuario.rol } });

    } catch (error) {
        console.error("❌ Error en el login:", error);
        res.status(500).json({ message: 'Error en el servidor', error });
    }
});

// Ruta para solicitar recuperación de contraseña
router.post('/recuperar-cuenta', async (req, res) => {
    const { email } = req.body;

    try {
        // Buscar usuario en la base de datos
        const usuario = await Usuario.findOne({ where: { email } });

        if (!usuario) {
            return res.status(404).json({ message: 'No existe ninguna cuenta con este correo.' });
        }

        // Generar código de recuperación de 6 dígitos
        const codigoRecuperacion = Math.floor(100000 + Math.random() * 900000).toString();
        console.log("Código generado:", codigoRecuperacion);  // <-- Agregar este log

        // Establecer tiempo de expiración (10 minutos desde ahora)
        const expiracionCodigo = moment().add(5, 'minutes').format('YYYY-MM-DD HH:mm:ss');
        console.log(`🕒 El código OTP expira a las: ${expiracionCodigo}`);

        // Guardar código y expiración en la base de datos
        const [filasActualizadas] = await Usuario.update(
            {
                codigo_recuperacion: codigoRecuperacion,
                expiracion_codigo: literal(`'${expiracionCodigo}'`)  // ← ✅ Aquí lo forzamos tal cual
            },
            { where: { email } }
        );

        // Verificar si realmente se guardó
        if (filasActualizadas > 0) {
            console.log(`✅ Código de recuperación guardado en la base de datos para ${email}: ${codigoRecuperacion}`);
        } else {
            console.error(`❌ No se pudo guardar el código en la base de datos para ${email}`);
        }

        // Consultar nuevamente el usuario para verificar que el código está guardado
        const usuarioActualizado = await Usuario.findOne({ where: { email } });
        console.log("📌 Código en BD después de actualizar:", usuarioActualizado.codigo_recuperacion);
        console.log("📌 Expiración en BD después de actualizar:", usuarioActualizado.expiracion_codigo);

        // Configurar transporte de correo
        const transporter = nodemailer.createTransport({
            host: process.env.EMAIL_HOST,
            port: process.env.EMAIL_PORT,
            secure: false,
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASS
            }
        });

        // Configurar correo electrónico
        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: email,
            subject: '🔐 Recuperación de cuenta - ReyBoxes',
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: #f8f9fa;">
                    <div style="text-align: center;">
                        <img src="https://scontent-mad1-1.xx.fbcdn.net/v/t39.30808-1/415751285_874525538008163_7351325140883369283_n.jpg?stp=dst-jpg_s200x200_tt6&_nc_cat=106&ccb=1-7&_nc_sid=2d3e12&_nc_ohc=Q_wgsHHpx2sQ7kNvgGK1c_B&_nc_oc=AdmyZBDIRwkBZpknf5Gzm834ojdZhh8Wn7jllEnHZ7cgNlFUNweEbfZocAaXC33Troc5QQdWWkzwSLDNjAfAhVtb&_nc_zt=24&_nc_ht=scontent-mad1-1.xx&_nc_gid=ysM0cfODDM8xcSfUO8ZX6w&oh=00_AYHmaswlJ02hb0OFRK88L91llLgyKubQOrVGM5QLgduWHg&oe=67E30EBC" alt="ReyBoxes" style="max-width: 200px; margin-bottom: 10px;">
                        <h2 style="color: #E30613;">Código de recuperación</h2>
                    </div>
                    <p style="font-size: 16px; color: #333;">
                        Hola, <strong>${email}</strong>,
                    </p>
                    <p style="font-size: 16px; color: #333;">
                        Recibimos una solicitud para restablecer tu contraseña en <strong>ReyBoxes</strong>. 
                        Usa el siguiente código para continuar con el proceso:
                    </p>
                    <div style="text-align: center; margin: 20px 0;">
                        <span style="font-size: 24px; font-weight: bold; color: #E30613; padding: 10px 20px; border: 2px dashed #E30613; border-radius: 5px; display: inline-block;">
                            ${codigoRecuperacion}
                        </span>
                    </div>
                    <p style="font-size: 16px; color: #333;">
                        Este código expirará en <strong>10 minutos</strong>.
                    </p>
                    <p style="font-size: 16px; color: #333;">
                        Si no solicitaste este código, ignora este correo. Tu cuenta sigue protegida.
                    </p>
                    <p style="font-size: 14px; color: #888; text-align: center;">
                        © 2024 ReyBoxes | Mecánica y mantenimiento
                    </p>
                </div>
            `
        };

        // Añadir logs para depuración
        console.log("Enviando correo a:", email);
        console.log("Contenido del correo:", mailOptions);

        // Enviar correo
        await transporter.sendMail(mailOptions);
        console.log("✅ Correo enviado correctamente");

        res.json({ message: 'Código de recuperación enviado al correo.' });

    } catch (error) {
        console.error("❌ Error al enviar el correo:", error);
        res.status(500).json({ message: 'Error enviando el correo.', error });
    }
});



// Ruta para verificar el código de recuperación
router.post('/verificar-codigo', async (req, res) => {
    const { email, codigo } = req.body;

    try {
        // Buscar usuario en la base de datos
        const usuario = await Usuario.findOne({ where: { email } });

        if (!usuario) {
            return res.status(404).json({ message: 'Usuario no encontrado.' });
        }

        // Verificar si el código ingresado coincide con el almacenado
        if (String(usuario.codigo_recuperacion) !== String(codigo)) {
            return res.status(400).json({ message: 'Código incorrecto o expirado.' });
        }

        // Verificar si el código ha expirado
        if (usuario.expiracion_codigo && moment().isAfter(usuario.expiracion_codigo)) {
            return res.status(400).json({ message: 'El código ha expirado. Solicita uno nuevo.' });
        }

        res.json({ message: 'Código verificado correctamente.' });

    } catch (error) {
        console.error("❌ Error al verificar el código:", error);
        res.status(500).json({ message: 'Error en el servidor', error });
    }
});

// Ruta para guardar la nueva contraseña
router.post('/nueva-contrasena', async (req, res) => {
    const { email, nuevaContrasena } = req.body;

    try {
        const usuario = await Usuario.findOne({ where: { email } });

        if (!usuario) {
            return res.status(404).json({ message: 'Usuario no encontrado.' });
        }

        // Hashear la nueva contraseña
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(nuevaContrasena, salt);

        // Actualizar contraseña y limpiar el código de recuperación
        await Usuario.update(
            {
                password: hashedPassword,
                codigo_recuperacion: null
            },
            { where: { email } }
        );

        res.json({ message: 'Contraseña actualizada correctamente.' });

    } catch (error) {
        console.error("❌ Error al cambiar la contraseña:", error);
        res.status(500).json({ message: 'Error al cambiar la contraseña.', error });
    }
});

export default router;
