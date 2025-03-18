import { Sequelize } from 'sequelize';
import dotenv from 'dotenv';

dotenv.config();

// Configuración de la conexión a PostgreSQL
const sequelize = new Sequelize(
    process.env.DB_NOMBRE,
    process.env.DB_USUARIO,
    process.env.DB_CONTRASENA,
    {
        host: process.env.DB_HOST,
        dialect: 'postgres',
        port: process.env.DB_PUERTO,
        dialectOptions: {
            ssl: {
                require: true,
                rejectUnauthorized: false
            }
        },
        logging: true // Desactivar logs de SQL en la consola
    }
);

// Probar conexión
(async () => {
    try {
        await sequelize.authenticate();
        console.log('✅ Conexión a PostgreSQL establecida correctamente.');
    } catch (error) {
        console.error('❌ Error al conectar a PostgreSQL:', error);
    }
})();

export { sequelize };
