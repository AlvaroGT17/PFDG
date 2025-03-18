import { DataTypes } from "sequelize";
import sequelize from "../config/database.js";

const Usuario = sequelize.define(
    "Usuario",
    {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
        },
        nombre: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        apellido: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        email: {
            type: DataTypes.STRING,
            allowNull: false,
            unique: true,
        },
        password: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        rol: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        created_at: {
            type: DataTypes.DATE,
            defaultValue: DataTypes.NOW,
            field: "created_at", // Forzamos el nombre correcto
        },
        updated_at: {
            type: DataTypes.DATE,
            defaultValue: DataTypes.NOW,
            field: "updated_at", // Forzamos el nombre correcto
        },
    },
    {
        tableName: "usuarios", // Nombre exacto de la tabla en la BD
        timestamps: false, // Evita que Sequelize use `createdAt` y `updatedAt`
        underscored: true, // Asegura que las columnas se usen en `snake_case`
    }
);

export default Usuario;
