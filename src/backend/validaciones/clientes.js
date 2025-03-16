const { check, validationResult } = require("express-validator");

const validarCliente = [
    check("nif")
        .notEmpty().withMessage("El NIF es obligatorio")
        .isLength({ min: 9, max: 9 }).withMessage("El NIF debe tener 9 caracteres"),
    check("nombre")
        .notEmpty().withMessage("El nombre es obligatorio")
        .isString().withMessage("El nombre debe ser un texto"),
    check("apellido1")
        .notEmpty().withMessage("El primer apellido es obligatorio"),
    check("email")
        .optional()
        .isEmail().withMessage("Debe ser un email válido"),
    check("telefono")
        .optional()
        .isMobilePhone("es-ES").withMessage("Debe ser un teléfono válido"),
    check("direccion")
        .optional()
        .isString().withMessage("Debe ser un texto"),
    check("localidad")
        .optional()
        .isString().withMessage("Debe ser un texto"),
    check("provincia")
        .optional()
        .isString().withMessage("Debe ser un texto"),
    check("codigo_postal")
        .optional()
        .isPostalCode("ES").withMessage("Debe ser un código postal válido"),

    // Middleware para manejar los errores
    (req, res, next) => {
        const errores = validationResult(req);
        if (!errores.isEmpty()) {
            return res.status(400).json({ errores: errores.array() });
        }
        next();
    }
];

module.exports = { validarCliente };
