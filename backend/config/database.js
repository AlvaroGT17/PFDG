import Sequelize from "sequelize";
import dotenv from "dotenv";

dotenv.config();

// Configuración de la conexión a PostgreSQL con IPv6
const sequelize = new Sequelize("postgres", "postgres", "AGT17021983BrfB", {
    host: "db.gxcexgzaavrffqqmwvxu.supabase.co",
    dialect: "postgres",
    dialectOptions: {
        ssl: {
            require: true,
            rejectUnauthorized: false,
        },
    },
    logging: false,
    define: {
        timestamps: false,
    },
});

// Probar conexión
(async () => {
    try {
        await sequelize.authenticate();
        console.log("✅ Conexión a PostgreSQL establecida correctamente.");
    } catch (error) {
        console.error("❌ Error al conectar a PostgreSQL:", error);
    }
})();

export default sequelize;
