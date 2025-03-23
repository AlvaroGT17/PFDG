// backend/controllers/authController.js
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import Usuario from '../models/Usuario.js';
import dotenv from 'dotenv';
import sequelize from '../config/database.js';

dotenv.config();

// ✅ REGISTRO DE USUARIO
export const registrarUsuario = async (req, res) => {
    let { nombre, apellido, email, password, rol } = req.body;

    try {
        nombre = nombre.toUpperCase();

        // Verificar si el correo ya existe
        const existe = await Usuario.findOne({ where: { email } });
        if (existe) {
            return res.status(400).json({ error: 'El correo ya está registrado' });
        }

        // Hashear la contraseña
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        // Crear nuevo usuario
        const nuevoUsuario = await Usuario.create({
            nombre,
            apellido,
            email,
            password: hashedPassword,
            rol
        });

        res.status(201).json({ mensaje: 'Usuario registrado exitosamente', usuario: nuevoUsuario });
    } catch (error) {
        console.error('Error en registrarUsuario:', error);
        res.status(500).json({ error: 'Error en el servidor' });
    }
};

// ✅ LOGIN POR NOMBRE
export const loginUsuario = async (req, res) => {
    let { nombre, password } = req.body;

    try {
        nombre = nombre.toUpperCase();

        const usuario = await Usuario.findOne({
            where: { nombre },
            attributes: ['id', 'nombre', 'apellido', 'email', 'password', 'rol'], // obligamos a traer solo lo necesario
            raw: true, // 🔁 fuerza a que Sequelize devuelva un objeto plano sin cachear
            logging: console.log // 👀 opcional, solo para ver la query SQL en consola
        });

        if (!usuario) {
            return res.status(401).json({ error: 'Credenciales incorrectas' });
        }

        const validPassword = await bcrypt.compare(password, usuario.password);
        if (!validPassword) {
            return res.status(401).json({ error: 'Credenciales incorrectas' });
        }

        const token = jwt.sign(
            { id: usuario.id, email: usuario.email, rol: usuario.rol },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );

        console.log(`✅ Login exitoso: ${usuario.nombre} - ${usuario.email}`);

        res.json({
            mensaje: 'Inicio de sesión exitoso',
            token,
            usuario: {
                id: usuario.id,
                nombre: usuario.nombre,
                apellido: usuario.apellido,
                email: usuario.email,
                rol: usuario.rol
            }
        });
    } catch (error) {
        console.error('Error en loginUsuario:', error);
        res.status(500).json({ error: 'Error en el servidor' });
    }
};

// ✅ CAMBIO DE CONTRASEÑA TRAS VERIFICACIÓN
export const cambiarContrasena = async (req, res) => {
    const { email, nuevaContrasena } = req.body;

    try {
        const usuario = await Usuario.findOne({ where: { email } });
        if (!usuario) {
            return res.status(404).json({ error: 'Usuario no encontrado.' });
        }

        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(nuevaContrasena, salt);

        await usuario.update({
            password: hashedPassword,
            codigo_recuperacion: null,
            expiracion_codigo: null,
            updated_at: new Date()
        });

        res.json({ mensaje: 'Contraseña actualizada correctamente.' });

        // 🔁 Cierra el pool para evitar cacheo de conexión en Electron
        await sequelize.connectionManager.close();

    } catch (error) {
        console.error('Error al cambiar la contraseña:', error);
        res.status(500).json({ error: 'Error al cambiar la contraseña' });
    }
};
