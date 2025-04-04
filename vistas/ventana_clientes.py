from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QToolButton, QVBoxLayout,
    QHBoxLayout, QScrollArea
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from utilidades.rutas import obtener_ruta_absoluta


class VentanaClientes(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Registrar cliente")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(620, 700)
        self.setObjectName("ventana_clientes")

        self.setup_ui()
        self.aplicar_estilos()

    def setup_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        # Título fijo
        self.titulo = QLabel()
        self.titulo.setObjectName("titulo_cliente")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.actualizar_titulo("")
        layout_principal.addWidget(self.titulo)

        # Contenedor para los campos con scroll
        contenedor = QWidget()
        contenedor.setObjectName("contenedor")
        layout_contenedor = QVBoxLayout(contenedor)
        layout_contenedor.setSpacing(12)

        # Campos del cliente
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")

        self.input_apellido1 = QLineEdit()
        self.input_apellido1.setPlaceholderText("Primer apellido")

        self.input_apellido2 = QLineEdit()
        self.input_apellido2.setPlaceholderText("Segundo apellido")

        self.input_dni = QLineEdit()
        self.input_dni.setPlaceholderText("DNI")

        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Teléfono")

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Correo electrónico")

        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Dirección")

        self.input_cp = QLineEdit()
        self.input_cp.setPlaceholderText("Código postal")

        self.input_localidad = QLineEdit()
        self.input_localidad.setPlaceholderText("Localidad")

        self.input_provincia = QLineEdit()
        self.input_provincia.setPlaceholderText("Provincia")

        self.input_observaciones = QTextEdit()
        self.input_observaciones.setPlaceholderText("Observaciones (opcional)")
        self.input_observaciones.setFixedHeight(80)

        # Añadir campos al layout del contenedor
        layout_contenedor.addWidget(self.input_nombre)
        layout_contenedor.addWidget(self.input_apellido1)
        layout_contenedor.addWidget(self.input_apellido2)
        layout_contenedor.addWidget(self.input_dni)
        layout_contenedor.addWidget(self.input_telefono)
        layout_contenedor.addWidget(self.input_email)
        layout_contenedor.addWidget(self.input_direccion)
        layout_contenedor.addWidget(self.input_cp)
        layout_contenedor.addWidget(self.input_localidad)
        layout_contenedor.addWidget(self.input_provincia)
        layout_contenedor.addWidget(self.input_observaciones)

        # Scroll solo para el formulario
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scroll_area")
        scroll.setWidget(contenedor)
        layout_principal.addWidget(scroll)

        # Botones fijos (fuera del scroll)
        layout_botones = QHBoxLayout()

        self.boton_guardar = QToolButton()
        self.boton_guardar.setText("Registrar")
        self.boton_guardar.setIconSize(QSize(48, 48))
        self.boton_guardar.setIcon(
            QIcon(obtener_ruta_absoluta("img/guardar.png")))
        self.boton_guardar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_limpiar = QToolButton()
        self.boton_limpiar.setText("Limpiar")
        self.boton_limpiar.setIconSize(QSize(48, 48))
        self.boton_limpiar.setIcon(
            QIcon(obtener_ruta_absoluta("img/escoba.png")))
        self.boton_limpiar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_volver = QToolButton()
        self.boton_volver.setText("Volver")
        self.boton_volver.setIconSize(QSize(48, 48))
        self.boton_volver.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_volver.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        layout_botones.addWidget(self.boton_guardar)
        layout_botones.addWidget(self.boton_limpiar)
        layout_botones.addWidget(self.boton_volver)

        layout_principal.addLayout(layout_botones)

        # Título dinámico con nombre
        self.input_nombre.textChanged.connect(self.actualizar_titulo)

    def aplicar_estilos(self):
        ruta_css = obtener_ruta_absoluta("css/clientes.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def actualizar_titulo(self, texto):
        nombre = texto.strip().upper()
        if nombre:
            self.titulo.setText(
                f"<span style='color: #FFFFFF;'>Registrar cliente </span>"
                f"<span style='color: #D90429;'>{nombre}</span>"
            )
        else:
            self.titulo.setText(
                "<span style='color: #FFFFFF;'>Registrar cliente</span>")
