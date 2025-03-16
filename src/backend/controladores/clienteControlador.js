const { validationResult, check } = require("express-validator");
const Cliente = require("../modelos/cliente");

// 📌 Función para validar NIF/NIE correctamente
const validarNIF_NIE = (nif) => {
    const letrasNIF = "TRWAGMYFPDXBNJZSQVHLCKE";
    const regexNIF = /^[0-9]{8}[A-Z]$/;
    const regexNIE = /^[XYZ][0-9]{7}[A-Z]$/;

    if (regexNIF.test(nif)) {
        const numero = parseInt(nif.substring(0, 8), 10);
        const letra = nif.charAt(8);
        return letrasNIF[numero % 23] === letra;
    } else if (regexNIE.test(nif)) {
        let numero = nif.substring(1, 8);
        switch (nif.charAt(0)) {
            case "X": numero = "0" + numero; break;
            case "Y": numero = "1" + numero; break;
            case "Z": numero = "2" + numero; break;
        }
        const letra = nif.charAt(8);
        return letrasNIF[parseInt(numero, 10) % 23] === letra;
    }
    return false;
};

// 📌 Middleware de validación para creación
const validarCliente = [
    check("nif")
        .notEmpty().withMessage("El NIF/NIE es obligatorio")
        .isLength({ min: 9, max: 9 }).withMessage("El NIF/NIE debe tener 9 caracteres")
        .custom((nif) => {
            if (!validarNIF_NIE(nif)) {
                throw new Error("El formato del NIF/NIE es incorrecto o la letra no es válida");
            }
            return true;
        })
        .custom(async (nif) => {
            const clienteExistente = await Cliente.findOne({ where: { nif } });
            if (clienteExistente) {
                throw new Error("El NIF/NIE ya está registrado");
            }
        }),

    check("nombre")
        .notEmpty().withMessage("El nombre es obligatorio")
        .matches(/^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$/).withMessage("El nombre solo puede contener letras"),

    check("apellido1")
        .notEmpty().withMessage("El primer apellido es obligatorio")
        .matches(/^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$/).withMessage("El primer apellido solo puede contener letras"),

    check("email")
        .notEmpty().withMessage("El email es obligatorio")
        .isEmail().withMessage("Debe ser un email válido"),

    check("telefono")
        .notEmpty().withMessage("El teléfono es obligatorio")
        .matches(/^[679]\d{8}$/).withMessage("Debe ser un teléfono válido en España"),

    check("codigo_postal")
        .optional()
        .matches(/^[0-9]{5}$/).withMessage("Debe ser un código postal válido en España"),
];

// 📌 Middleware de validación para actualización (PUT)
const validarActualizacionCliente = [
    check("nif")
        .optional()
        .isLength({ min: 9, max: 9 }).withMessage("El NIF/NIE debe tener 9 caracteres")
        .custom((nif) => {
            if (nif && !validarNIF_NIE(nif)) {
                throw new Error("El formato del NIF/NIE es incorrecto o la letra no es válida");
            }
            return true;
        }),

    check("nombre")
        .optional()
        .matches(/^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$/).withMessage("El nombre solo puede contener letras"),

    check("apellido1")
        .optional()
        .matches(/^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$/).withMessage("El primer apellido solo puede contener letras"),

    check("email")
        .optional()
        .isEmail().withMessage("Debe ser un email válido"),

    check("telefono")
        .optional()
        .matches(/^[679]\d{8}$/).withMessage("Debe ser un teléfono válido en España"),

    check("codigo_postal")
        .optional()
        .matches(/^[0-9]{5}$/).withMessage("Debe ser un código postal válido en España"),
];

// 📌 Obtener todos los clientes
const obtenerClientes = async (req, res) => {
    try {
        const clientes = await Cliente.findAll();
        res.json({ exito: true, mensaje: "Clientes obtenidos correctamente", datos: clientes });
    } catch (error) {
        res.status(500).json({ exito: false, mensaje: "Error al obtener los clientes", error: error.message });
    }
};

// 📌 Obtener un cliente por ID
const obtenerClientePorId = async (req, res) => {
    try {
        const cliente = await Cliente.findByPk(req.params.id);
        if (!cliente) {
            return res.status(404).json({ exito: false, mensaje: "Cliente no encontrado" });
        }
        res.json({ exito: true, mensaje: "Cliente encontrado", datos: cliente });
    } catch (error) {
        res.status(500).json({ exito: false, mensaje: "Error al obtener el cliente", error: error.message });
    }
};

// 📌 Crear un cliente
const crearCliente = async (req, res) => {
    const errores = validationResult(req);
    if (!errores.isEmpty()) {
        return res.status(400).json({
            exito: false,
            errores: errores.array().map(err => ({ campo: err.path, mensaje: err.msg }))
        });
    }

    try {
        const cliente = await Cliente.create(req.body);
        res.status(201).json({ exito: true, mensaje: "Cliente creado correctamente", datos: cliente });
    } catch (error) {
        res.status(500).json({ exito: false, mensaje: "Error al crear el cliente", error: error.message });
    }
};

// 📌 Actualizar un cliente
const actualizarCliente = async (req, res) => {
    const errores = validationResult(req);
    if (!errores.isEmpty()) {
        return res.status(400).json({
            exito: false,
            errores: errores.array().map(err => ({ campo: err.path, mensaje: err.msg }))
        });
    }

    try {
        const cliente = await Cliente.findByPk(req.params.id);
        if (!cliente) {
            return res.status(404).json({ exito: false, mensaje: "Cliente no encontrado" });
        }

        await cliente.update(req.body);
        res.json({ exito: true, mensaje: "Cliente actualizado correctamente", datos: cliente });
    } catch (error) {
        res.status(500).json({ exito: false, mensaje: "Error al actualizar el cliente", error: error.message });
    }
};

// 📌 Eliminar un cliente
const eliminarCliente = async (req, res) => {
    try {
        const cliente = await Cliente.findByPk(req.params.id);
        if (!cliente) {
            return res.status(404).json({ exito: false, mensaje: "Cliente no encontrado" });
        }

        await cliente.destroy();
        res.json({ exito: true, mensaje: "Cliente eliminado correctamente" });
    } catch (error) {
        res.status(500).json({ exito: false, mensaje: "Error al eliminar el cliente", error: error.message });
    }
};

module.exports = {
    validarCliente,
    validarActualizacionCliente,
    obtenerClientes,
    obtenerClientePorId,
    crearCliente,
    actualizarCliente,
    eliminarCliente
};
