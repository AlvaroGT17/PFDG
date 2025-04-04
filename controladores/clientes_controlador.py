from PySide6.QtWidgets import QMessageBox
from vistas.ventana_clientes import VentanaClientes
from modelos.clientes_consultas import crear_cliente, dni_ya_existe
from utilidades.comprobar_dni import DNIUtils
import re


class ClientesControlador:
    def __init__(self, ventana_anterior):
        self.ventana = VentanaClientes()
        self.ventana_anterior = ventana_anterior

        self.ventana.boton_volver.clicked.connect(self.volver)
        self.ventana.boton_limpiar.clicked.connect(self.limpiar_campos)
        self.ventana.boton_guardar.clicked.connect(self.registrar_cliente)

        self.ventana.show()

    def volver(self):
        self.ventana.close()
        self.ventana_anterior.show()

    def limpiar_campos(self):
        self.ventana.input_nombre.clear()
        self.ventana.input_apellido1.clear()
        self.ventana.input_apellido2.clear()
        self.ventana.input_dni.clear()
        self.ventana.input_telefono.clear()
        self.ventana.input_email.clear()
        self.ventana.input_direccion.clear()
        self.ventana.input_cp.clear()
        self.ventana.input_localidad.clear()
        self.ventana.input_provincia.clear()
        self.ventana.input_observaciones.clear()

    def registrar_cliente(self):
        nombre = self.ventana.input_nombre.text().strip()
        apellido1 = self.ventana.input_apellido1.text().strip()
        apellido2 = self.ventana.input_apellido2.text().strip()
        raw_dni = self.ventana.input_dni.text().strip()
        dni = re.sub(r'[^A-Za-z0-9]', '', raw_dni).upper()
        telefono = self.ventana.input_telefono.text().strip()
        email = self.ventana.input_email.text().strip()
        direccion = self.ventana.input_direccion.text().strip()
        cp = self.ventana.input_cp.text().strip()
        localidad = self.ventana.input_localidad.text().strip()
        provincia = self.ventana.input_provincia.text().strip()
        observaciones = self.ventana.input_observaciones.toPlainText().strip()

        # Validaciones básicas
        if not nombre or not apellido1 or not dni:
            self.mostrar_error(
                "Nombre, primer apellido y DNI son obligatorios.")
            return

        if email and not self.validar_email(email):
            self.mostrar_error(
                "El correo electrónico no tiene un formato válido.")
            return

        # ✅ Validar formato y letra del DNI
        if not DNIUtils.validar_dni(dni):
            self.mostrar_error("El DNI introducido no es válido.")
            return

        if dni_ya_existe(dni):
            self.mostrar_error("Ya existe un cliente con ese DNI.")
            return

        exito = crear_cliente(
            nombre, apellido1, apellido2, dni, telefono, email,
            direccion, cp, localidad, provincia, observaciones
        )

        if exito:
            self.mostrar_info("Cliente registrado correctamente.")
            self.limpiar_campos()
        else:
            self.mostrar_error("Ocurrió un error al registrar el cliente.")

    def validar_email(self, email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email)

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self.ventana, "Error", mensaje)

    def mostrar_info(self, mensaje):
        QMessageBox.information(self.ventana, "Información", mensaje)
