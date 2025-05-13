"""
Módulo de interfaz gráfica para la verificación de código de recuperación.

Esta ventana se muestra tras solicitar el código por correo. Permite al usuario
introducir el código recibido y verificarlo antes de continuar al restablecimiento
de contraseña. Incluye un campo de texto, icono, botón de verificación, volver,
y una etiqueta con cuenta atrás visible.

Estilo y diseño visual cargados desde un archivo CSS externo.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QCursor
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from utilidades.rutas import obtener_ruta_absoluta


class VentanaVerificar(QWidget):
    """
    Clase que representa la ventana de verificación de código.

    Contiene un campo de entrada para el código de 6 dígitos, un contador
    con el tiempo restante antes de la expiración, y botones para verificar
    o volver al login.
    """

    def __init__(self):
        """
        Inicializa la ventana de verificación.

        - Establece el título, icono, tamaño y estilo visual.
        - Llama al método para construir y organizar la interfaz.
        """
        super().__init__()
        self.setWindowTitle("ReyBoxes - Verificar código")
        self.setFixedSize(375, 360)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))

        ruta_css = obtener_ruta_absoluta("css/verificar_codigo.css")
        with open(ruta_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.inicializar_ui()

    def inicializar_ui(self):
        """
        Construye y organiza los elementos de la interfaz.

        Incluye:
        - Título y subtítulo informativo.
        - Campo de entrada para el código con icono.
        - Etiqueta para la cuenta atrás.
        - Botones de verificación y volver con sus respectivos iconos.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 15, 30, 10)
        layout.setSpacing(10)

        titulo = QLabel(
            '<span style="color:#333;">Verificar </span><span style="color:#d90429;">Código</span>')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo_verificar")
        layout.addWidget(titulo)

        subtitulo = QLabel("Introduce el código que recibiste por correo:")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setObjectName("texto_instruccion")
        layout.addWidget(subtitulo)

        fila_codigo = QHBoxLayout()
        icono = QLabel()
        icono.setPixmap(QPixmap(obtener_ruta_absoluta(
            "img/codigo.png")).scaled(24, 24, Qt.KeepAspectRatio))
        icono.setFixedWidth(30)
        icono.setAlignment(Qt.AlignCenter)

        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Introduce tu código")
        self.input_codigo.setFixedHeight(34)
        self.input_codigo.setMaxLength(6)
        self.input_codigo.setAlignment(Qt.AlignCenter)
        self.input_codigo.setToolTip("Código de 6 dígitos enviado por correo")

        fila_codigo.addWidget(icono)
        fila_codigo.addWidget(self.input_codigo)
        layout.addLayout(fila_codigo)

        # Cuenta atrás
        self.label_tiempo = QLabel("El código expira en: 5:00")
        self.label_tiempo.setAlignment(Qt.AlignCenter)
        self.label_tiempo.setStyleSheet("font-size: 14px; color: black;")
        self.label_tiempo.setObjectName("cuenta_atras")
        layout.addWidget(self.label_tiempo)

        contenedor_botones = QHBoxLayout()
        contenedor_botones.setSpacing(12)

        self.btn_verificar = QPushButton("  Verificar")
        self.btn_verificar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_verificar.setIcon(
            QIcon(obtener_ruta_absoluta("img/verificar.png")))

        self.btn_volver = QPushButton("  Volver")
        self.btn_volver.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_volver.setIcon(QIcon(obtener_ruta_absoluta("img/volver.png")))

        contenedor_botones.addWidget(self.btn_verificar)
        contenedor_botones.addWidget(self.btn_volver)

        layout.addLayout(contenedor_botones)
