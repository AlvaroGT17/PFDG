const express = require("express");
const { registrarUsuario, iniciarSesion } = require("../controladores/authControlador");

const router = express.Router();

router.post("/register", registrarUsuario);
router.post("/login", iniciarSesion);

module.exports = router;
