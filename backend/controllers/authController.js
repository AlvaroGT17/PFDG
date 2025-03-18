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

// Registro de usuario con apellido y rol
exports.registrarUsuario = async (req, res) => {
    const { nombre, apellido, email, password, rol } = req.body;

    try {
        // Verificar si el usuario ya existe
        const existeUsuario = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);

        if (existeUsuario.rows.length > 0) {
            return res.status(400).json({ error: 'El correo ya está registrado' });
        }

        // Encriptar la contraseña
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        // Guardar usuario en la base de datos
        const nuevoUsuario = await pool.query(
            'INSERT INTO usuarios (nombre, apellido, email, password, rol, created_at, updated_at) VALUES ($1, $2, $3, $4, $5, NOW(), NOW()) RETURNING *',
            [nombre, apellido, email, hashedPassword, rol]
        );

        res.status(201).json({ mensaje: 'Usuario registrado exitosamente', usuario: nuevoUsuario.rows[0] });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error en el servidor' });
    }
};

// Inicio de sesión
exports.loginUsuario = async (req, res) => {
    const { email, password } = req.body;

    try {
        // Buscar usuario por email
        const usuario = await pool.query('SELECT * FROM usuarios WHERE email = $1', [email]);

        if (usuario.rows.length === 0) {
            return res.status(401).json({ error: 'Credenciales incorrectas' });
        }

        // Comparar contraseñas
        const validPassword = await bcrypt.compare(password, usuario.rows[0].password);
        if (!validPassword) {
            return res.status(401).json({ error: 'Credenciales incorrectas' });
        }

        // Crear token JWT
        const token = jwt.sign(
            { id: usuario.rows[0].id, email: usuario.rows[0].email, rol: usuario.rows[0].rol },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );

        res.json({ mensaje: 'Inicio de sesión exitoso', token, usuario: usuario.rows[0] });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error en el servidor' });
    }
};
