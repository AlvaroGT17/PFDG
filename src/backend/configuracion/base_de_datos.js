// src/backend/configuracion/base_de_datos.js

const { Sequelize } = require('sequelize');
require('dotenv').config();

// Configuración de Sequelize usando variables de entorno
const sequelize = new Sequelize(
    process.env.DB_NOMBRE,     // Nombre de la base de datos
    process.env.DB_USUARIO,    // Usuario de la base de datos
    process.env.DB_CONTRASENA, // Contraseña de la base de datos
    {
        host: process.env.DB_HOST,      // Host de la base de datos (por ejemplo, db.tu_proyecto.supabase.co)
        port: process.env.DB_PUERTO || 5432, // Puerto (5432 es el predeterminado para PostgreSQL)
        dialect: 'postgres',            // Especificamos que usaremos PostgreSQL
        logging: false,                 // Desactiva la salida de logs en la consola (opcional)
        dialectOptions: {
            ssl: process.env.DB_SSL === 'true' ? {
                require: true,
                rejectUnauthorized: false
            } : false
        }
    }
);

// Función para autenticar la conexión a la base de datos
async function conectarBaseDeDatos() {
    try {
        await sequelize.authenticate();
        console.log('Conexión a la base de datos establecida correctamente.');
    } catch (error) {
        console.error('No se pudo conectar a la base de datos:', error);
    }
}

module.exports = {
    sequelize,
    conectarBaseDeDatos
};
