import sys
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import QPropertyAnimation, QRect, QTimer
from utilidades.rutas import obtener_ruta_absoluta
from vistas.ventana_login import VentanaLogin


class VentanaPresentacion(QWidget):
    """
    Ventana de presentación (splash screen) que se muestra al iniciar la aplicación.

    Esta ventana:
    - Es transparente y sin bordes.
    - Muestra una animación donde el logo se expande desde el centro hasta ocupar el espacio completo.
    - Permanece visible unos segundos y luego da paso a la ventana de login.

    Forma parte de la experiencia visual de inicio para reforzar la identidad visual de la aplicación ReyBoxes.
    """

    def __init__(self):
        """
        Inicializa la ventana de presentación con animación del logo.

        La ventana se configura como sin marco, en primer plano y con fondo transparente.
        Se inicia una animación que agranda el logo desde el centro hasta una posición visible.
        """
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(1000, 700)

        # Logo
        self.logo = QLabel(self)
        ruta_logo = obtener_ruta_absoluta("img/logo.jpg")
        pixmap = QPixmap(ruta_logo)
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
        self.logo.setGeometry(500, 350, 0, 0)

        # Animación del logo
        self.animacion = QPropertyAnimation(self.logo, b"geometry")
        self.animacion.setDuration(1500)
        self.animacion.setStartValue(QRect(500, 350, 0, 0))
        self.animacion.setEndValue(QRect(150, 117, 700, 466))
        self.animacion.finished.connect(self.esperar_y_cambiar)

        self.animacion.start()

    def esperar_y_cambiar(self):
        """
        Espera una pequeña fracción de tiempo tras finalizar la animación y luego lanza la ventana de login.
        """
        QTimer.singleShot(30, self.mostrar_login)

    def mostrar_login(self):
        """
        Muestra la ventana de login y cierra la ventana de presentación.

        Al finalizar la animación, esta función crea una instancia de VentanaLogin,
        la muestra en pantalla y cierra la ventana de presentación actual.
        """
        self.login = VentanaLogin()
        self.login.show()
        self.close()
