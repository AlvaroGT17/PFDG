import express from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import Usuario from '../models/Usuario.js';
import dotenv from 'dotenv';
import nodemailer from 'nodemailer';
import enviarCorreo from '../util/emailService.js';

dotenv.config();
const router = express.Router();

// Ruta para manejar el login
router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        // Buscar usuario en la base de datos
        const usuario = await Usuario.findOne({ where: { email } });

        if (!usuario) {
            return res.status(404).json({ message: 'Usuario no encontrado' });
        }

        // Verificar contraseña
        const validPassword = await bcrypt.compare(password, usuario.password);
        if (!validPassword) {
            return res.status(401).json({ message: 'Contraseña incorrecta' });
        }

        // Generar token JWT
        const token = jwt.sign(
            { id: usuario.id, email: usuario.email, rol: usuario.rol },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );

        res.json({ token, usuario: { id: usuario.id, nombre: usuario.nombre, apellido: usuario.apellido, email: usuario.email, rol: usuario.rol } });
    } catch (error) {
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

        // Guardar código en la base de datos de manera explícita
        const [filasActualizadas] = await Usuario.update(
            { codigo_recuperacion: codigoRecuperacion },
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
            subject: 'Código de recuperación de contraseña',
            text: `Tu código de recuperación es: ${codigoRecuperacion}.`
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
        if (usuario.codigo_recuperacion !== codigo) {
            return res.status(400).json({ message: 'Código incorrecto o expirado.' });
        }

        res.json({ message: 'Código verificado correctamente.' });

    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Error en el servidor', error });
    }
});

export default router;
