const express = require("express");
const cors = require("cors");
require("dotenv").config();

const clienteRutas = require("./rutas/clienteRutas");
const authRutas = require("./rutas/authRutas");

const app = express();

app.use(express.json());
app.use(cors());

app.use("/api", clienteRutas);
app.use("/api/auth", authRutas);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`✅ Servidor corriendo en http://localhost:${PORT}`);
});
