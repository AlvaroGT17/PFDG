from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QToolButton, QVBoxLayout,
    QHBoxLayout, QComboBox, QFrame
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta
from PySide6.QtCore import Qt, QSize


class VentanaUsuarios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Crear usuario")
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.setFixedSize(500, 600)
        self.setObjectName("ventana_usuarios")

        self.setup_ui()
        self.aplicar_estilos()

    def setup_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)

        contenedor = QFrame()
        contenedor.setObjectName("contenedor")
        contenedor.setFrameShape(QFrame.StyledPanel)
        layout_contenedor = QVBoxLayout(contenedor)
        layout_contenedor.setSpacing(15)

        self.titulo = QLabel()
        self.titulo.setObjectName("titulo_usuario")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.actualizar_titulo("")

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")

        self.input_apellido = QLineEdit()
        self.input_apellido.setPlaceholderText("Apellido")

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Correo electrónico")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.input_repetir = QLineEdit()
        self.input_repetir.setPlaceholderText("Repetir contraseña")
        self.input_repetir.setEchoMode(QLineEdit.Password)

        self.combo_rol = QComboBox()
        self.combo_rol.setPlaceholderText("Selecciona un rol")

        self.boton_crear = QToolButton()
        self.boton_crear.setText("Crear usuario")
        self.boton_crear.setIcon(QIcon(obtener_ruta_absoluta("img/crear.png")))
        self.boton_crear.setIconSize(QSize(48, 48))
        self.boton_crear.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_limpiar = QToolButton()
        self.boton_limpiar.setText("Limpiar")
        self.boton_limpiar.setIcon(
            QIcon(obtener_ruta_absoluta("img/escoba.png")))
        self.boton_limpiar.setIconSize(QSize(48, 48))
        self.boton_limpiar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.boton_volver = QToolButton()
        self.boton_volver.setText("Volver")
        self.boton_volver.setIcon(
            QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.boton_volver.setIconSize(QSize(48, 48))
        self.boton_volver.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_crear)
        layout_botones.addWidget(self.boton_limpiar)
        layout_botones.addWidget(self.boton_volver)

        layout_contenedor.addWidget(self.titulo)
        layout_contenedor.addWidget(self.input_nombre)
        layout_contenedor.addWidget(self.input_apellido)
        layout_contenedor.addWidget(self.input_email)
        layout_contenedor.addWidget(self.input_password)
        layout_contenedor.addWidget(self.input_repetir)
        layout_contenedor.addWidget(self.combo_rol)
        layout_contenedor.addLayout(layout_botones)

        layout_principal.addWidget(contenedor, alignment=Qt.AlignCenter)

        # Conectar señal de cambio de nombre
        self.input_nombre.textChanged.connect(self.actualizar_titulo)

    def aplicar_estilos(self):
        ruta_css = obtener_ruta_absoluta("css/usuarios.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def actualizar_titulo(self, texto):
        nombre = texto.strip().upper()
        if nombre:
            self.titulo.setText(
                f"<span style='color: #FFFFFF;'>Crear usuario </span>"
                f"<span style='color: #D90429;'>{nombre}</span>"
            )
        else:
            self.titulo.setText(
                "<span style='color: #FFFFFF;'>Crear usuario</span>")
