from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta


class BotonAnimado(QPushButton):
    def __init__(self, texto, icono):
        super().__init__()

        self.setObjectName("boton_menu")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(140, 100)

        # Icono
        icon_path = obtener_ruta_absoluta(f"img/{icono}")
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(
            38, 38, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)

        # Texto
        texto_label = QLabel(texto)
        texto_label.setAlignment(Qt.AlignCenter)
        texto_label.setStyleSheet(
            "color: white; font-size: 14px; font-weight: bold;")

        # Layout interno
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(icon_label)
        layout.addWidget(texto_label)
