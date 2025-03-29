from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QCursor, QIcon
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta


class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Inicio de sesión")
        self.setFixedSize(500, 600)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))

        ruta_estilo = obtener_ruta_absoluta("css/login.css")
        with open(ruta_estilo, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.input_usuario = None
        self.input_contrasena = None
        self.btn_entrar = None
        self.enlace_recuperar = None

        self.inicializar_ui()

    def inicializar_ui(self):
        layout_general = QVBoxLayout(self)
        layout_general.setContentsMargins(0, 20, 0, 20)
        layout_general.setSpacing(10)

        logo = QLabel()
        ruta_logo = obtener_ruta_absoluta("img/logo.jpg")
        logo.setPixmap(QPixmap(ruta_logo).scaled(
            400, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout_general.addWidget(logo)

        panel = QWidget()
        panel.setObjectName("panel_central")
        panel.setFixedWidth(440)

        layout_panel = QVBoxLayout(panel)
        layout_panel.setContentsMargins(30, 30, 30, 30)
        layout_panel.setSpacing(20)

        titulo = QLabel(
            '<span style="color:#333;">Iniciar </span><span style="color:#d90429;">Sesión</span>')
        titulo.setObjectName("titulo_principal")
        titulo.setAlignment(Qt.AlignCenter)
        layout_panel.addWidget(titulo)

        layout_panel.addLayout(self.crear_campo(
            "img/usuario.png", "Inserte su nombre", es_password=False))
        layout_panel.addLayout(self.crear_campo(
            "img/candado.png", "Contraseña", es_password=True))

        self.btn_entrar = QPushButton("  Entrar")
        icono_llave = QPixmap(obtener_ruta_absoluta(
            "img/llave.png")).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.btn_entrar.setIcon(icono_llave)
        self.btn_entrar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_entrar.setFixedWidth(200)
        layout_panel.addWidget(self.btn_entrar, alignment=Qt.AlignCenter)

        self.enlace_recuperar = QLabel(
            '<a href="#">¿Olvidaste tu contraseña?</a>')
        self.enlace_recuperar.setProperty("enlace", True)
        self.enlace_recuperar.setAlignment(Qt.AlignCenter)
        self.enlace_recuperar.setTextInteractionFlags(
            Qt.TextBrowserInteraction)
        self.enlace_recuperar.setOpenExternalLinks(False)
        layout_panel.addWidget(self.enlace_recuperar)

        layout_general.addWidget(panel, alignment=Qt.AlignCenter)

    def crear_campo(self, ruta_icono, placeholder, es_password=False):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        icono = QLabel()
        icono.setPixmap(QPixmap(obtener_ruta_absoluta(ruta_icono)).scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icono.setFixedWidth(30)
        icono.setAlignment(Qt.AlignCenter)

        input_texto = QLineEdit()
        input_texto.setPlaceholderText(placeholder)
        input_texto.setFixedHeight(36)
        if es_password:
            input_texto.setEchoMode(QLineEdit.Password)
            self.input_contrasena = input_texto
        else:
            self.input_usuario = input_texto

        layout.addWidget(icono)
        layout.addWidget(input_texto)
        return layout
