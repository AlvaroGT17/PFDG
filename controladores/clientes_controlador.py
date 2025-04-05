from PySide6.QtWidgets import QMessageBox, QCompleter
from PySide6.QtCore import Qt, QEvent, QObject
from vistas.ventana_clientes import VentanaClientes
from modelos.clientes_consultas import (
    crear_cliente,
    dni_ya_existe,
    buscar_clientes_por_nombre,
    obtener_cliente_por_id,
    obtener_clientes as obtener_todos_los_clientes,
    actualizar_cliente
)
from utilidades.comprobar_dni import DNIUtils
import re


class ClientesControlador(QObject):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.setObjectName("controlador_clientes")
        self.ventana = VentanaClientes()
        self.ventana_anterior = ventana_anterior

        self.ventana.boton_volver.clicked.connect(self.volver)
        self.ventana.boton_limpiar.clicked.connect(self.limpiar_campos)
        self.ventana.boton_guardar.clicked.connect(self.registrar_cliente)
        self.ventana.boton_modificar.clicked.connect(self.modificar_cliente)
        self.ventana.boton_modificar.setEnabled(False)
        self.ventana.boton_eliminar.clicked.connect(self.eliminar_cliente)
        self.ventana.boton_eliminar.setEnabled(False)

        self.lista_clientes = obtener_todos_los_clientes()
        self.cliente_seleccionado_id = None

        # Diccionarios para búsquedas
        self.dict_nombres = {}
        self.dict_dnis = {}
        self.dict_telefonos = {}

        for cliente in self.lista_clientes:
            nombre_completo = f"{cliente['nombre']} {cliente['primer_apellido']} {cliente.get('segundo_apellido', '')}".strip(
            )
            self.dict_nombres[nombre_completo] = cliente
            self.dict_dnis[cliente['dni']] = cliente
            if cliente['telefono']:
                self.dict_telefonos[cliente['telefono']] = cliente

        # Completers
        completer_nombre = QCompleter(list(self.dict_nombres.keys()))
        completer_nombre.setCaseSensitivity(Qt.CaseInsensitive)
        completer_nombre.setFilterMode(Qt.MatchContains)
        self.ventana.input_buscar_nombre.setCompleter(completer_nombre)
        self.ventana.input_buscar_nombre.installEventFilter(self)

        completer_dni = QCompleter(list(self.dict_dnis.keys()))
        completer_dni.setCaseSensitivity(Qt.CaseInsensitive)
        completer_dni.setFilterMode(Qt.MatchContains)
        self.ventana.input_buscar_dni.setCompleter(completer_dni)
        self.ventana.input_buscar_dni.installEventFilter(self)

        completer_tel = QCompleter(list(self.dict_telefonos.keys()))
        completer_tel.setCaseSensitivity(Qt.CaseInsensitive)
        completer_tel.setFilterMode(Qt.MatchContains)
        self.ventana.input_buscar_telefono.setCompleter(completer_tel)
        self.ventana.input_buscar_telefono.installEventFilter(self)

        self.ventana.show()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if source == self.ventana.input_buscar_nombre:
                texto = source.text().strip()
                cliente = self.dict_nombres.get(texto)
                if cliente:
                    self.rellenar_campos(cliente)
                    return True
            elif source == self.ventana.input_buscar_dni:
                texto = source.text().strip().upper()
                cliente = self.dict_dnis.get(texto)
                if cliente:
                    self.rellenar_campos(cliente)
                    return True
            elif source == self.ventana.input_buscar_telefono:
                texto = source.text().strip()
                cliente = self.dict_telefonos.get(texto)
                if cliente:
                    self.rellenar_campos(cliente)
                    return True
        return super().eventFilter(source, event)

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
        self.ventana.input_buscar_nombre.clear()
        self.ventana.input_buscar_dni.clear()
        self.ventana.input_buscar_telefono.clear()
        self.ventana.boton_modificar.setEnabled(False)
        self.cliente_seleccionado_id = None

    def registrar_cliente(self):
        nombre = self.ventana.input_nombre.text().strip()
        apellido1 = self.ventana.input_apellido1.text().strip()
        apellido2 = self.ventana.input_apellido2.text().strip()
        dni = self.ventana.input_dni.text().strip()
        telefono = self.ventana.input_telefono.text().strip()
        email = self.ventana.input_email.text().strip()
        direccion = self.ventana.input_direccion.text().strip()
        cp = self.ventana.input_cp.text().strip()
        localidad = self.ventana.input_localidad.text().strip()
        provincia = self.ventana.input_provincia.text().strip()
        observaciones = self.ventana.input_observaciones.toPlainText().strip()

        if not nombre or not apellido1 or not dni:
            self.mostrar_error(
                "Nombre, primer apellido y DNI son obligatorios.")
            return

        if not DNIUtils.validar_dni(dni):
            self.mostrar_error("El DNI introducido no es válido.")
            return

        if email and not self.validar_email(email):
            self.mostrar_error(
                "El correo electrónico no tiene un formato válido.")
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

    def rellenar_campos(self, cliente):
        self.cliente_seleccionado_id = cliente["id"]
        self.ventana.boton_modificar.setEnabled(True)
        self.ventana.boton_eliminar.setEnabled(True)

        self.ventana.input_nombre.setText(cliente["nombre"])
        self.ventana.input_apellido1.setText(cliente["primer_apellido"])
        self.ventana.input_apellido2.setText(cliente["segundo_apellido"])
        self.ventana.input_dni.setText(cliente["dni"])
        self.ventana.input_telefono.setText(cliente["telefono"] or "")
        self.ventana.input_email.setText(cliente["email"] or "")
        self.ventana.input_direccion.setText(cliente["direccion"] or "")
        self.ventana.input_cp.setText(cliente["codigo_postal"] or "")
        self.ventana.input_localidad.setText(cliente["localidad"] or "")
        self.ventana.input_provincia.setText(cliente["provincia"] or "")
        self.ventana.input_observaciones.setText(
            cliente["observaciones"] or "")

    def validar_email(self, email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email)

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self.ventana, "Error", mensaje)

    def mostrar_info(self, mensaje):
        QMessageBox.information(self.ventana, "Información", mensaje)

    def modificar_cliente(self):
        if not self.cliente_seleccionado_id:
            self.mostrar_error(
                "Primero debes buscar y seleccionar un cliente.")
            return

        nombre = self.ventana.input_nombre.text().strip()
        apellido1 = self.ventana.input_apellido1.text().strip()
        apellido2 = self.ventana.input_apellido2.text().strip()
        dni = self.ventana.input_dni.text().strip()
        telefono = self.ventana.input_telefono.text().strip()
        email = self.ventana.input_email.text().strip()
        direccion = self.ventana.input_direccion.text().strip()
        cp = self.ventana.input_cp.text().strip()
        localidad = self.ventana.input_localidad.text().strip()
        provincia = self.ventana.input_provincia.text().strip()
        observaciones = self.ventana.input_observaciones.toPlainText().strip()

        cliente_original = next(
            (c for c in self.lista_clientes if c["id"] == self.cliente_seleccionado_id), None)

        if not cliente_original:
            self.mostrar_error("No se ha podido obtener el cliente original.")
            return

        dni_original = cliente_original["dni"]

        if dni != dni_original:
            if not DNIUtils.validar_dni(dni):
                self.mostrar_error("El DNI introducido no es válido.")
                return
            if dni_ya_existe(dni):
                self.mostrar_error("Ya existe un cliente con ese DNI.")
                return

        if email and not self.validar_email(email):
            self.mostrar_error(
                "El correo electrónico no tiene un formato válido.")
            return

        exito = actualizar_cliente(
            self.cliente_seleccionado_id,
            nombre, apellido1, apellido2, dni, telefono, email,
            direccion, cp, localidad, provincia, observaciones
        )

        if exito:
            self.mostrar_info("Cliente modificado correctamente.")
            self.limpiar_campos()
        else:
            self.mostrar_error("Ocurrió un error al modificar el cliente.")

    def eliminar_cliente(self):
        if not self.cliente_seleccionado_id:
            self.mostrar_error(
                "Primero debes seleccionar un cliente para eliminar.")
            return

        confirmacion = QMessageBox.question(
            self.ventana,
            "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar este cliente?\nEsta acción no eliminará sus reparaciones ni vehículos.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            from modelos.clientes_consultas import eliminar_cliente_por_id

            exito = eliminar_cliente_por_id(self.cliente_seleccionado_id)
            if exito:
                self.mostrar_info("Cliente eliminado correctamente.")
                self.limpiar_campos()
                self.ventana.input_buscar_nombre.clear()
                self.ventana.input_buscar_dni.clear()
                self.ventana.input_buscar_telefono.clear()
                self.ventana.boton_modificar.setEnabled(False)
                self.ventana.boton_eliminar.setEnabled(False)
                self.cliente_seleccionado_id = None
                self.lista_clientes = obtener_todos_los_clientes()
            else:
                self.mostrar_error("Error al eliminar el cliente.")

    def volver(self):
        self.ventana.close()
        self.ventana.deleteLater()
        self.ventana_anterior.show()
