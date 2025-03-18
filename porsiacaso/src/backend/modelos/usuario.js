const { DataTypes } = require('sequelize');
const { sequelize } = require('../configuracion/base_de_datos');
const bcrypt = require("bcryptjs");

const Usuario = sequelize.define('Usuario', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    nombre: {
        type: DataTypes.STRING(100),
        allowNull: false
    },
    apellido: {  // 🔹 Agregado para que coincida con la BD
        type: DataTypes.STRING(100),
        allowNull: false
    },
    email: {
        type: DataTypes.STRING(150),
        allowNull: false,
        unique: true,
        validate: {
            isEmail: { msg: 'Debe ser un email válido' }
        }
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false
    },
    rol: { // 🔹 Asegurar que el rol también esté en el modelo
        type: DataTypes.STRING(50),
        allowNull: false,
        defaultValue: 'cliente'
    }
}, {
    tableName: 'usuarios',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
    //hooks: {
    //   beforeCreate: async (usuario) => {
    //        usuario.password = await bcrypt.hash(usuario.password, 10);
    //    }
    //}
});

module.exports = Usuario;
