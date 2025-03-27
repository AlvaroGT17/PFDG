from utilidades.rutas import obtener_ruta_absoluta
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QCursor, QIcon, QFontDatabase
from PySide6.QtCore import Qt, Signal


class VentanaPrincipal(QWidget):
    senal_abrir_recuperacion = Signal()

    def __init__(self):
        super().__init__()

        # Cargar fuente Montserrat
        QFontDatabase.addApplicationFont(obtener_ruta_absoluta(
            "font/Montserrat-Italic-VariableFont_wght.ttf"))

        self.setWindowTitle("ReyBoxes - Inicio de sesión")
        self.setFixedSize(500, 600)

        # Favicon personalizado
        ruta_icono = obtener_ruta_absoluta("img/favicon.ico")
        self.setWindowIcon(QIcon(ruta_icono))

        # Cargar estilos desde archivo externo
        ruta_estilo = obtener_ruta_absoluta("css/login.css")
        with open(ruta_estilo, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.inicializar_ui()

    def inicializar_ui(self):
        layout_general = QVBoxLayout(self)
        layout_general.setContentsMargins(0, 20, 0, 20)
        layout_general.setSpacing(10)

        # Logo
        logo = QLabel()
        ruta_logo = obtener_ruta_absoluta("img/logo.jpg")
        logo.setPixmap(QPixmap(ruta_logo).scaled(
            400, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout_general.addWidget(logo)

        # Panel central
        panel = QWidget()
        panel.setObjectName("panel_central")
        panel.setFixedWidth(440)

        layout_panel = QVBoxLayout(panel)
        layout_panel.setContentsMargins(30, 30, 30, 30)
        layout_panel.setSpacing(20)

        # Título
        titulo = QLabel(
            '<span style="color:#333;">Iniciar </span><span style="color:#d90429;">Sesión</span>')
        titulo.setObjectName("titulo_principal")
        titulo.setAlignment(Qt.AlignCenter)
        layout_panel.addWidget(titulo)

        # Campo usuario
        layout_panel.addLayout(self.crear_campo(
            "img/usuario.png", "Inserte su nombre"))

        # Campo contraseña
        layout_panel.addLayout(self.crear_campo(
            "img/candado.png", "Contraseña", es_password=True))

        # Botón Entrar
        btn_entrar = QPushButton("  Entrar")
        icono_llave = QPixmap(obtener_ruta_absoluta(
            "img/llave.png")).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        btn_entrar.setIcon(icono_llave)
        btn_entrar.setCursor(QCursor(Qt.PointingHandCursor))
        btn_entrar.setFixedWidth(200)
        layout_panel.addWidget(btn_entrar, alignment=Qt.AlignCenter)

        # Enlace recuperar contraseña
        enlace = QLabel('<a href="#">¿Olvidaste tu contraseña?</a>')
        enlace.setProperty("enlace", True)
        enlace.setAlignment(Qt.AlignCenter)
        enlace.setTextInteractionFlags(Qt.TextBrowserInteraction)
        enlace.setOpenExternalLinks(False)
        enlace.linkActivated.connect(self.lanzar_recuperacion)
        layout_panel.addWidget(enlace)

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

        layout.addWidget(icono)
        layout.addWidget(input_texto)
        return layout

    def lanzar_recuperacion(self):
        print("🛠 Abrir ventana de recuperación")
        self.senal_abrir_recuperacion.emit()
