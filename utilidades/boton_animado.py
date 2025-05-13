"""
Módulo que define el widget personalizado `BotonAnimado` para el menú principal de la aplicación.

Este botón combina un icono centrado y un texto estilizado debajo, con apariencia visual uniforme.
Está diseñado para integrarse en interfaces con diseño de cuadrícula, como el Dashboard de ReyBoxes.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from utilidades.rutas import obtener_ruta_absoluta


class BotonAnimado(QPushButton):
    """
    Botón personalizado con icono e información textual, utilizado en el menú principal.

    A diferencia de un QPushButton convencional, este botón contiene internamente un layout vertical
    con un icono escalado y un texto centrado. Se ajusta a un tamaño fijo y cambia el cursor al pasar
    por encima para indicar interactividad.
    """

    def __init__(self, texto, icono):
        """
        Inicializa el botón con el texto y el icono proporcionados.

        Args:
            texto (str): Texto que se mostrará debajo del icono.
            icono (str): Nombre del archivo de icono (relativo a la carpeta 'img/').
        """
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
