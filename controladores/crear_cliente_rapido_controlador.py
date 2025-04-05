from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from vistas.ventana_crear_cliente_rapido import VentanaCrearClienteRapido
from modelos.clientes_consultas import dni_ya_existe, crear_cliente, crear_cliente_y_devolver_id
from utilidades.comprobar_dni import DNIUtils


class CrearClienteRapidoControlador(QObject):
    cliente_creado = Signal(dict)

    def __init__(self, ventana_padre=None):
        super().__init__()
        self.ventana = VentanaCrearClienteRapido()

        self.ventana.boton_crear.clicked.connect(self.crear_cliente)
        self.ventana.boton_cancelar.clicked.connect(self.ventana.close)

        self.ventana.show()

    def crear_cliente(self):
        nombre = self.ventana.input_nombre.text().strip().upper()
        apellido1 = self.ventana.input_apellido1.text().strip().upper()
        apellido2 = ""
        dni = self.ventana.input_dni.text().strip().upper()
        telefono = self.ventana.input_telefono.text().strip()
        email = direccion = cp = localidad = provincia = observaciones = ""

        if not DNIUtils.validar_dni(dni):
            self.mostrar_mensaje(
                "El DNI introducido no es válido.", "DNI no válido", exito=False)
            return

        if dni_ya_existe(dni):
            self.mostrar_mensaje(
                "Ya existe un cliente con este DNI.", "DNI duplicado", exito=False)
            return

        nuevo_id = crear_cliente_y_devolver_id(
            nombre, apellido1, apellido2, dni, telefono, email,
            direccion, cp, localidad, provincia, observaciones
        )

        if nuevo_id:
            self.mostrar_mensaje(
                "Cliente creado correctamente.", "Éxito", exito=True)
            self.cliente_creado.emit({
                "id": nuevo_id,
                "nombre": nombre,
                "primer_apellido": apellido1,
                "segundo_apellido": apellido2,
                "dni": dni,
                "telefono": telefono,
                "email": email
            })
            self.ventana.close()
        else:
            self.mostrar_mensaje(
                "No se pudo crear el cliente.", "Error", exito=False)

    def mostrar_mensaje(self, texto, titulo, exito=True):
        msg = QMessageBox(self.ventana)
        msg.setIcon(QMessageBox.Information if exito else QMessageBox.Critical)
        msg.setText(texto)
        msg.setWindowTitle(titulo)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("""
            QLabel { color: black; font-weight: bold; }
            QPushButton {
                background-color: #E30613;
                color: white;
                border-radius: 12px;
                padding: 6px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c10510;
            }
        """)
        msg.exec()
