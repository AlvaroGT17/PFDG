"""
Módulo para la ventana de inicio de sesión de la aplicación ReyBoxes.

Esta interfaz permite al usuario:
- Iniciar sesión con nombre de usuario y contraseña.
- Acceder al sistema de recuperación de cuenta.
- Salir de la aplicación mediante un botón controlado.

Incluye validación visual, iconografía y un diseño centrado, con estilos
personalizados mediante archivo CSS.
"""

from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtGui import QPixmap, QCursor, QIcon
from PySide6.QtCore import Qt, QCoreApplication
from utilidades.rutas import obtener_ruta_absoluta


class VentanaLogin(QWidget):
    """
    Ventana principal de inicio de sesión del sistema ReyBoxes.

    Permite al usuario:
    - Introducir su nombre de usuario y contraseña.
    - Iniciar sesión mediante el botón "Entrar".
    - Acceder al sistema de recuperación de contraseña.
    - Salir de la aplicación de forma controlada.

    La ventana bloquea el cierre mediante el botón de aspa (❌) para forzar un cierre controlado.
    """

    def __init__(self):
        """
        Inicializa la interfaz gráfica de la ventana de login, cargando estilos, logo y campos de entrada.
        """
        super().__init__()
        self.setWindowTitle("ReyBoxes - Inicio de sesión")
        self.setFixedSize(500, 600)
        self.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))
        self.cierre_autorizado = False

        ruta_estilo = obtener_ruta_absoluta("css/login.css")
        with open(ruta_estilo, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.input_usuario = None
        self.input_contrasena = None
        self.btn_entrar = None
        self.enlace_recuperar = None

        self.inicializar_ui()

    def inicializar_ui(self):
        """
        Configura todos los elementos gráficos de la ventana: logo, campos de entrada,
        botones de acción y enlace para recuperación de contraseña.
        """
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

        # Campos de usuario y contraseña
        layout_panel.addLayout(self.crear_campo(
            "img/usuario.png", "Inserte su nombre", es_password=False))
        layout_panel.addLayout(self.crear_campo(
            "img/candado.png", "Contraseña", es_password=True))

        # Botón Entrar
        self.btn_entrar = QPushButton("  Entrar")
        icono_llave = QPixmap(obtener_ruta_absoluta(
            "img/llave.png")).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.btn_entrar.setIcon(icono_llave)
        self.btn_entrar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_entrar.setFixedWidth(200)
        layout_panel.addWidget(self.btn_entrar, alignment=Qt.AlignCenter)

        # Botón Salir
        self.btn_salir = QPushButton("  Salir")
        self.btn_salir.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_salir.setIcon(QIcon(obtener_ruta_absoluta("img/salir.png")))
        self.btn_salir.clicked.connect(self.salir_aplicacion)
        layout_panel.addWidget(self.btn_salir, alignment=Qt.AlignCenter)

        # Enlace recuperación
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
        """
        Crea un campo de entrada compuesto por un icono y un QLineEdit.

        Args:
            ruta_icono (str): Ruta relativa del icono a mostrar.
            placeholder (str): Texto que se mostrará como sugerencia.
            es_password (bool): Indica si el campo es de contraseña (oculta los caracteres).

        Returns:
            QHBoxLayout: Layout horizontal con el icono y el campo de entrada.
        """
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

    def closeEvent(self, event):
        """
        Sobrescribe el evento de cierre de la ventana para bloquear el cierre con el botón (❌).

        Solo permite cerrar si la variable "cierre_autorizado" está activada (True).
        En caso contrario, muestra un mensaje informativo.

        Args:
            event (QCloseEvent): Evento de cierre de la ventana.
        """
        if not self.cierre_autorizado:
            QMessageBox.information(
                self,
                "Cierre no permitido",
                "Utiliza el botón 'Salir' para cerrar el programa.",
                QMessageBox.StandardButton.Ok
            )
            event.ignore()
        else:
            event.accept()

    def salir_aplicacion(self):
        """
        Permite cerrar la aplicación de forma controlada mediante el botón "Salir".

        Establece la variable "cierre_autorizado" como True y procede al cierre de la ventana.
        """
        self.cierre_autorizado = True
        self.close()
