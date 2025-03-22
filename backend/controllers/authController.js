const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
    user: process.env.DB_USUARIO,
    host: process.env.DB_HOST,
    database: process.env.DB_NOMBRE,
    password: process.env.DB_CONTRASENA,
    port: process.env.DB_PUERTO,
    ssl: { rejectUnauthorized: false }
});

// ✅ REGISTRO DE USUARIO
exports.registrarUsuario = async (req, res) => {
    let { nombre, apellido, email, password, rol } = req.body;

    try {
        // Asegurar que el nombre se guarda en mayúsculas
        nombre = nombre.toUpperCase();

        // Verificar si el correo ya está registrado
        const existeUsuario = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);
        if (existeUsuario.rows.length > 0) {
            return res.status(400).json({ error: 'El correo ya está registrado' });
        }

        // Encriptar la contraseña
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        // Insertar el usuario en la base de datos
        const nuevoUsuario = await pool.query(
            'INSERT INTO usuarios (nombre, apellido, email, password, rol, created_at, updated_at) VALUES ($1, $2, $3, $4, $5, NOW(), NOW()) RETURNING *',
            [nombre, apellido, email, hashedPassword, rol]
        );

        res.status(201).json({ mensaje: 'Usuario registrado exitosamente', usuario: nuevoUsuario.rows[0] });
    } catch (error) {
        console.error('Error en registrarUsuario:', error);
        res.status(500).json({ error: 'Error en el servidor' });
    }
};

// ✅ LOGIN POR NOMBRE
exports.loginUsuario = async (req, res) => {
    let { nombre, password } = req.body;

    try {
        // Convertir nombre a mayúsculas para comparar
        nombre = nombre.toUpperCase();

        // Buscar usuario por nombre
        const usuario = await pool.query('SELECT * FROM usuarios WHERE nombre = $1', [nombre]);
        if (usuario.rows.length === 0) {
            return res.status(401).json({ error: 'Credenciales incorrectas' });
        }

        // Validar contraseña
        const validPassword = await bcrypt.compare(password, usuario.rows[0].password);
        if (!validPassword) {
            return res.status(401).json({ error: 'Credenciales incorrectas' });
        }

        // Generar token
        const token = jwt.sign(
            {
                id: usuario.rows[0].id,
                email: usuario.rows[0].email,
                rol: usuario.rows[0].rol
            },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );

        res.json({ mensaje: 'Inicio de sesión exitoso', token, usuario: usuario.rows[0] });
    } catch (error) {
        console.error('Error en loginUsuario:', error);
        res.status(500).json({ error: 'Error en el servidor' });
    }
};
