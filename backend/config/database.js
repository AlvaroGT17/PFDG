import Sequelize from "sequelize";
import dotenv from "dotenv";
dotenv.config();

const { DB_NOMBRE, DB_USUARIO, DB_CONTRASENA, DB_HOST, DB_PUERTO, DB_SSL } = process.env;

const connectionString = `postgresql://${DB_USUARIO}:${DB_CONTRASENA}@${DB_HOST}:${DB_PUERTO}/${DB_NOMBRE}`;

const sequelize = new Sequelize(connectionString, {
    dialect: "postgres",
    dialectOptions: {
        ssl: DB_SSL === "true"
            ? { require: true, rejectUnauthorized: false }
            : false,
    },
    logging: false,
    define: {
        timestamps: false,
    },
});

export default sequelize;
