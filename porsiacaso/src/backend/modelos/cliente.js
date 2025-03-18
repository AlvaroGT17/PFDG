const { DataTypes } = require('sequelize');
const { sequelize } = require('../configuracion/base_de_datos');

// Función para validar NIF y NIE
function validarNIF_NIE(valor) {
    const letrasDNI = "TRWAGMYFPDXBNJZSQVHLCKE"; // Letras válidas para NIF

    if (!valor) throw new Error("El NIF/NIE es obligatorio");

    // Validar NIF (DNI con letra correcta)
    if (/^\d{8}[A-Z]$/.test(valor)) {
        const numero = parseInt(valor.slice(0, 8), 10);
        const letra = valor.slice(-1);
        if (letrasDNI[numero % 23] !== letra) {
            throw new Error("La letra del NIF es incorrecta");
        }
        return true;
    }

    // Validar NIE (Empieza por X, Y o Z + 7 números + 1 letra)
    if (/^[XYZ]\d{7}[A-Z]$/.test(valor)) {
        let numero = valor.replace("X", "0").replace("Y", "1").replace("Z", "2");
        numero = parseInt(numero.slice(0, 8), 10);
        const letra = valor.slice(-1);
        if (letrasDNI[numero % 23] !== letra) {
            throw new Error("La letra del NIE es incorrecta");
        }
        return true;
    }

    throw new Error("Formato de NIF/NIE incorrecto");
}

const Cliente = sequelize.define('Cliente', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    nif: {
        type: DataTypes.STRING(9),
        unique: true,
        allowNull: false,
        validate: {
            validarNIF_NIE
        }
    },
    nombre: {
        type: DataTypes.STRING(100),
        allowNull: false,
        validate: {
            notNull: { msg: 'El nombre es obligatorio' },
            is: {
                args: /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/,
                msg: "El nombre solo puede contener letras"
            }
        }
    },
    apellido1: {
        type: DataTypes.STRING(100),
        allowNull: false,
        validate: {
            notNull: { msg: 'El primer apellido es obligatorio' },
            is: {
                args: /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/,
                msg: "El primer apellido solo puede contener letras"
            }
        }
    },
    apellido2: {
        type: DataTypes.STRING(100),
        allowNull: true,
        validate: {
            is: {
                args: /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/,
                msg: "El segundo apellido solo puede contener letras"
            }
        }
    },
    email: {
        type: DataTypes.STRING(150),
        allowNull: true,
        validate: {
            isEmail: { msg: 'Debe ser un email válido' }
        }
    },
    telefono: {
        type: DataTypes.STRING(20),
        allowNull: true,
        validate: {
            is: {
                args: /^[679]{1}[0-9]{8}$/,
                msg: "Debe ser un número de teléfono válido"
            }
        }
    },
    direccion: {
        type: DataTypes.STRING(200),
        allowNull: true,
        validate: {
            is: {
                args: /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ,.\s-]+$/,
                msg: "La dirección contiene caracteres inválidos"
            }
        }
    },
    localidad: {
        type: DataTypes.STRING(100),
        allowNull: true,
        validate: {
            is: {
                args: /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]+$/,
                msg: "La localidad solo puede contener letras y espacios"
            }
        }
    },
    provincia: {
        type: DataTypes.STRING(100),
        allowNull: true,
        validate: {
            is: {
                args: /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]+$/,
                msg: "La provincia solo puede contener letras y espacios"
            }
        }
    },
    codigo_postal: {
        type: DataTypes.STRING(5),
        allowNull: true,
        validate: {
            is: {
                args: /^[0-9]{5}$/,
                msg: "Debe ser un código postal válido (5 dígitos)"
            }
        }
    }
}, {
    tableName: 'clientes',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at'
});

module.exports = Cliente;
