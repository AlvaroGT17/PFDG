require("dotenv").config();
const express = require("express");
const cors = require("cors");

const clienteRutas = require("./rutas/clienteRutas");

const app = express();

// Middlewares
app.use(express.json());
app.use(cors());

// Ruta de prueba
app.get("/", (req, res) => {
    res.send("🚀 Servidor funcionando correctamente.");
});

// Cargar rutas
app.use("/api", clienteRutas);

module.exports = app; // Exporta para ser usado en server.js
