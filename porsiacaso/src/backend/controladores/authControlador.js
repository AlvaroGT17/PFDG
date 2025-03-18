const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const Usuario = require("../modelos/usuario");

const registrarUsuario = async (req, res) => {
    try {
        const { nombre, apellido, email, password } = req.body;

        // Verificar si el usuario ya existe
        const usuarioExistente = await Usuario.findOne({ where: { email } });
        if (usuarioExistente) {
            return res.status(400).json({ exito: false, mensaje: "El email ya está registrado" });
        }

        // 🔹 Hashear la contraseña (solo aquí)
        const hashedPassword = await bcrypt.hash(password, 10);

        // Crear usuario con contraseña hasheada
        const nuevoUsuario = await Usuario.create({
            nombre,
            apellido,
            email,
            password: hashedPassword
        });

        res.status(201).json({ exito: true, mensaje: "Usuario registrado correctamente", datos: nuevoUsuario });
    } catch (error) {
        res.status(500).json({ exito: false, mensaje: "Error al registrar el usuario", error: error.message });
    }
};

// 📌 Función para iniciar sesión
const iniciarSesion = async (req, res) => {
    try {
        console.log("➡ Recibido en /auth/login:", req.body);  // 👀 Verificar lo que llega

        const { email, password } = req.body;

        // Verificar si el usuario existe
        const usuario = await Usuario.findOne({ where: { email } });
        if (!usuario) {
            return res.status(401).json({ exito: false, mensaje: "Email o contraseña incorrectos" });
        }

        // Comparar contraseñas
        const esValida = await bcrypt.compare(password, usuario.password);
        if (!esValida) {
            return res.status(401).json({ exito: false, mensaje: "Email o contraseña incorrectos" });
        }

        // Generar token JWT
        const token = jwt.sign(
            { id: usuario.id, email: usuario.email },
            process.env.JWT_SECRET,
            { expiresIn: "1h" }
        );

        console.log("✅ Inicio de sesión exitoso para:", email);
        res.json({ exito: true, mensaje: "Inicio de sesión exitoso", token });

    } catch (error) {
        console.error("🔥 Error en el servidor:", error.message);
        res.status(500).json({ exito: false, mensaje: "Error en el servidor", error: error.message });
    }
};

// 📌 Exportar funciones
module.exports = { registrarUsuario, iniciarSesion };
