"""
Módulo de interfaz gráfica para restablecer la contraseña en el sistema ReyBoxes.

Contiene la clase VentanaRestaurar, que permite al usuario introducir una nueva
contraseña tras el proceso de recuperación, con una interfaz clara y segura.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from utilidades.rutas import obtener_ruta_absoluta


class VentanaRestaurar(QWidget):
    """
    Ventana gráfica para establecer una nueva contraseña del usuario.

    Permite ingresar una nueva contraseña y repetirla para confirmación.
    Se acompaña de botones para guardar los cambios o volver atrás.
    """

    def __init__(self):
        """
        Inicializa la ventana, carga estilos y configura la interfaz.
        """
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
        """
        Crea y organiza los elementos visuales de la interfaz de restablecimiento.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 20)
        layout.setSpacing(15)

        titulo = QLabel(
            '<span style="color:#333;">Nueva </span><span style="color:#d90429;">Contraseña</span>')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_restaurar")
        layout.addWidget(titulo)

        self.input_nueva = QLineEdit()
        self.input_nueva.setEchoMode(QLineEdit.Password)
        self.input_nueva.setPlaceholderText("Nueva contraseña")
        self.input_nueva.setToolTip("Introduce la nueva contraseña")
        layout.addWidget(self.input_nueva)

        self.input_repetir = QLineEdit()
        self.input_repetir.setEchoMode(QLineEdit.Password)
        self.input_repetir.setPlaceholderText("Repetir contraseña")
        self.input_repetir.setToolTip("Vuelve a escribir la nueva contraseña")
        layout.addWidget(self.input_repetir)

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
