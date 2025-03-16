const express = require("express");
const {
    validarCliente,
    validarActualizacionCliente,
    obtenerClientes,
    crearCliente,
    obtenerClientePorId,
    actualizarCliente,
    eliminarCliente
} = require("../controladores/clienteControlador");

const router = express.Router();

router.get("/clientes", obtenerClientes);
router.get("/clientes/:id", obtenerClientePorId);
router.post("/clientes", validarCliente, crearCliente);
router.put("/clientes/:id", validarActualizacionCliente, actualizarCliente);
router.delete("/clientes/:id", eliminarCliente);

module.exports = router;
