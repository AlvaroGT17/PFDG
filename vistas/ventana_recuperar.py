"""
Módulo para la ventana de recuperación de cuenta de usuario.

Permite al usuario introducir su correo electrónico para
recibir un código de verificación y proceder al restablecimiento de contraseña.

Incluye una interfaz gráfica amigable, con campos validados, iconos informativos
y botones accesibles para continuar o volver al inicio.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCursor, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from utilidades.rutas import obtener_ruta_absoluta


class VentanaRecuperar(QWidget):
    """
    Ventana gráfica para el proceso de recuperación de cuenta mediante correo electrónico.

    Permite al usuario:
    - Introducir su correo registrado.
    - Solicitar el envío de un código de verificación.
    - Volver a la pantalla de inicio de sesión.

    Atributos:
        input_correo (QLineEdit): Campo de entrada para el correo del usuario.
        btn_enviar (QPushButton): Botón para enviar el código de verificación.
        btn_volver (QPushButton): Botón para regresar al login.
    """

    def __init__(self):
        """
        Inicializa la ventana de recuperación de cuenta.

        Carga la hoja de estilo personalizada, define el diseño
        y crea los controles de interacción con el usuario.
        """
        super().__init__()
        self.setWindowTitle("ReyBoxes - Recuperar cuenta")
        self.setFixedSize(500, 300)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))

        # Aplicar estilo desde archivo CSS
        ruta_estilo = obtener_ruta_absoluta("css/recuperar.css")
        with open(ruta_estilo, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.input_correo = None
        self.btn_enviar = None
        self.btn_volver = None

        self.inicializar_ui()

    def inicializar_ui(self):
        """
        Configura y organiza los elementos visuales de la ventana.

        Incluye:
        - Título con estilo.
        - Texto de instrucción.
        - Campo de correo electrónico con icono.
        - Botones de acción: Enviar Código y Volver.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título principal
        titulo = QLabel(
            '<span style="color:#333;">Recuperar </span><span style="color:#d90429;">cuenta</span>')
        titulo.setObjectName("titulo_recuperar")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setContentsMargins(0, 0, 0, 4)
        layout.addWidget(titulo)

        # Texto de instrucción
        instruccion = QLabel(
            "Introduce el correo electrónico asociado a tu cuenta:")
        instruccion.setObjectName("texto_instruccion")
        instruccion.setAlignment(Qt.AlignLeft)
        instruccion.setContentsMargins(0, 0, 0, 4)
        layout.addWidget(instruccion)

        # Campo de entrada con icono
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

        # Botones: Enviar código y Volver
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
