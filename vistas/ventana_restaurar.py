from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QIcon, QPixmap, QCursor
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta


class VentanaRestaurar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReyBoxes - Nueva contraseña")
        self.setFixedSize(400, 360)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))

        # Estilo visual
        ruta_css = obtener_ruta_absoluta("css/restaurar.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.inicializar_ui()

    def inicializar_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 20)
        layout.setSpacing(15)

        # Título
        titulo = QLabel(
            '<span style="color:#333;">Nueva </span><span style="color:#d90429;">Contraseña</span>')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_restaurar")
        layout.addWidget(titulo)

        # Campo nueva contraseña
        self.input_nueva = QLineEdit()
        self.input_nueva.setEchoMode(QLineEdit.Password)
        self.input_nueva.setPlaceholderText("Nueva contraseña")
        self.input_nueva.setToolTip("Introduce la nueva contraseña")
        layout.addWidget(self.input_nueva)

        # Campo repetir contraseña
        self.input_repetir = QLineEdit()
        self.input_repetir.setEchoMode(QLineEdit.Password)
        self.input_repetir.setPlaceholderText("Repetir contraseña")
        self.input_repetir.setToolTip("Vuelve a escribir la nueva contraseña")
        layout.addWidget(self.input_repetir)

        # Botones
        botones = QHBoxLayout()
        self.btn_guardar = QPushButton("  Guardar")
        self.btn_guardar.setIcon(QIcon(obtener_ruta_absoluta("img/llave.png")))
        self.btn_guardar.setCursor(QCursor(Qt.PointingHandCursor))

        self.btn_volver = QPushButton("  Volver")
        self.btn_volver.setIcon(QIcon(obtener_ruta_absoluta("img/volver.png")))
        self.btn_volver.setCursor(QCursor(Qt.PointingHandCursor))

        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_volver)

        layout.addLayout(botones)
