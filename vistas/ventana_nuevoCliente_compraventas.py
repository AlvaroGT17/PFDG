from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
from modelos.nuevoCliente_compraventa_consulta import crear_cliente_y_devolver_id, dni_ya_existe
from utilidades.rutas import obtener_ruta_absoluta


class VentanaNuevoClienteCompraventas(QWidget):
    """
    Ventana para registrar un nuevo cliente en el contexto de compraventas.

    Esta ventana permite al usuario introducir los datos personales y de contacto de un nuevo cliente,
    validar campos obligatorios, comprobar duplicidad de DNI, y guardar la información en la base de datos.
    Dispone de dos botones principales: "Crear cliente" y "Cancelar".
    """

    def __init__(self, callback_guardar=None):
        """
        Inicializa la interfaz gráfica de la ventana para crear un nuevo cliente.

        Parámetros:
            callback_guardar (función, opcional): Función de retorno que se ejecuta al guardar el cliente,
            recibiendo como argumento el ID del cliente creado.
        """
        super().__init__()
        self.setWindowTitle("Nuevo Cliente - ReyBoxes")
        self.setFixedSize(500, 600)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setObjectName("ventana_nuevo_cliente")
        self.callback_guardar = callback_guardar

        with open(obtener_ruta_absoluta("css/nuevo_cliente.css"), "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout(self)

        titulo = QLabel(
            "<h2><span style='color:#738496;'>Rey</span><span style='color:#E30613;'>Boxes</span> - Nuevo Cliente</h2>")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        formulario = QFormLayout()

        self.nombre = QLineEdit()
        self.primer_apellido = QLineEdit()
        self.segundo_apellido = QLineEdit()
        self.dni = QLineEdit()
        self.telefono = QLineEdit()
        self.email = QLineEdit()
        self.direccion = QLineEdit()
        self.codigo_postal = QLineEdit()
        self.localidad = QLineEdit()
        self.provincia = QLineEdit()
        self.observaciones = QTextEdit()
        self.observaciones.setFixedHeight(60)

        formulario.addRow("Nombre:", self.nombre)
        formulario.addRow("Primer apellido:", self.primer_apellido)
        formulario.addRow("Segundo apellido:", self.segundo_apellido)
        formulario.addRow("DNI:", self.dni)
        formulario.addRow("Teléfono:", self.telefono)
        formulario.addRow("Email:", self.email)
        formulario.addRow("Dirección:", self.direccion)
        formulario.addRow("Código Postal:", self.codigo_postal)
        formulario.addRow("Localidad:", self.localidad)
        formulario.addRow("Provincia:", self.provincia)
        formulario.addRow("Observaciones:", self.observaciones)

        layout.addLayout(formulario)

        botones = QHBoxLayout()
        self.boton_guardar = QPushButton("Crear cliente")
        self.boton_guardar.setObjectName("boton_compraventa")
        self.boton_guardar.clicked.connect(self.crear_cliente)

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.setObjectName("boton_compraventa")
        self.boton_cancelar.clicked.connect(self.close)

        botones.addStretch()
        botones.addWidget(self.boton_guardar)
        botones.addWidget(self.boton_cancelar)
        layout.addLayout(botones)

    def crear_cliente(self):
        """
        Procesa los datos introducidos por el usuario para crear un nuevo cliente.

        Realiza las siguientes validaciones y acciones:
        - Verifica que los campos obligatorios (nombre, primer apellido, DNI y teléfono) estén completos.
        - Comprueba si el DNI ya existe en la base de datos.
        - Si todo es correcto, registra al nuevo cliente usando la función `crear_cliente_y_devolver_id()`.
        - Si se pasa un callback, lo ejecuta con el ID del nuevo cliente.
        - Muestra mensajes de información o error mediante cuadros de diálogo.
        """
        nombre = self.nombre.text().strip().upper()
        apellido1 = self.primer_apellido.text().strip().upper()
        dni = self.dni.text().strip().upper()
        telefono = self.telefono.text().strip()

        if not nombre or not apellido1 or not dni or not telefono:
            QMessageBox.warning(self, "Campos obligatorios",
                                "Por favor, rellena todos los campos obligatorios: nombre, apellido, DNI y teléfono.")
            return

        if dni_ya_existe(dni):
            QMessageBox.warning(self, "DNI duplicado",
                                "Ya existe un cliente con este DNI. Por favor, revisa los datos.")
            return

        datos = {
            "nombre": nombre,
            "primer_apellido": apellido1,
            "segundo_apellido": self.segundo_apellido.text().strip().upper(),
            "dni": dni,
            "telefono": telefono,
            "email": self.email.text().strip(),
            "direccion": self.direccion.text().strip(),
            "codigo_postal": self.codigo_postal.text().strip(),
            "localidad": self.localidad.text().strip(),
            "provincia": self.provincia.text().strip(),
            "observaciones": self.observaciones.toPlainText().strip()
        }

        nuevo_id = crear_cliente_y_devolver_id(**datos)

        if nuevo_id:
            QMessageBox.information(self, "Cliente creado",
                                    f"Cliente creado correctamente con ID {nuevo_id}.")
            if self.callback_guardar:
                self.callback_guardar(nuevo_id)
            self.close()
        else:
            QMessageBox.critical(self, "Error",
                                 "Ha ocurrido un error al crear el cliente. Inténtalo de nuevo.")
