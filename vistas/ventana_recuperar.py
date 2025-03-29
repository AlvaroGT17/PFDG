from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QCursor, QIcon
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta


class VentanaRecuperar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Recuperar cuenta")
        self.setFixedSize(500, 300)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))

        ruta_estilo = obtener_ruta_absoluta("css/recuperar.css")
        with open(ruta_estilo, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.input_correo = None
        self.btn_enviar = None
        self.btn_volver = None

        self.inicializar_ui()

    def inicializar_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        titulo = QLabel(
            '<span style="color:#333;">Recuperar </span><span style="color:#d90429;">cuenta</span>')
        titulo.setObjectName("titulo_recuperar")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setContentsMargins(0, 0, 0, 4)
        layout.addWidget(titulo)

        instruccion = QLabel(
            "Introduce el correo electrónico asociado a tu cuenta:")
        instruccion.setObjectName("texto_instruccion")
        instruccion.setAlignment(Qt.AlignLeft)
        instruccion.setContentsMargins(0, 0, 0, 4)
        layout.addWidget(instruccion)

        campo_layout = QHBoxLayout()
        campo_layout.setSpacing(8)

        icono = QLabel()
        icono.setPixmap(QPixmap(obtener_ruta_absoluta(
            "img/correo.png")).scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icono.setAlignment(Qt.AlignCenter)
        icono.setToolTip("Correo electrónico asociado a tu cuenta")

        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Introduce tu correo...")
        self.input_correo.setFixedHeight(32)
        self.input_correo.setToolTip(
            "Introduce aquí tu correo para enviarte un código de verificación")

        campo_layout.addWidget(icono)
        campo_layout.addWidget(self.input_correo)
        layout.addLayout(campo_layout)
        layout.setAlignment(campo_layout, Qt.AlignHCenter)

        layout.addSpacing(10)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(15)

        self.btn_enviar = QPushButton("  Enviar Código")
        self.btn_enviar.setIcon(QIcon(obtener_ruta_absoluta("img/codigo.png")))
        self.btn_enviar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_enviar.setEnabled(False)
        self.btn_enviar.setToolTip(
            "Introduce un correo válido para poder enviar el código")
        botones_layout.addWidget(self.btn_enviar)

        self.btn_volver = QPushButton("  Volver")
        self.btn_volver.setIcon(QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.btn_volver.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_volver.setToolTip("Volver a la pantalla de inicio de sesión")
        botones_layout.addWidget(self.btn_volver)

        layout.addLayout(botones_layout)
        layout.setAlignment(botones_layout, Qt.AlignHCenter)
