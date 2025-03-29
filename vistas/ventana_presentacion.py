import sys
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtCore import QPropertyAnimation, QRect, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QApplication
from utilidades.rutas import obtener_ruta_absoluta
from vistas.ventana_login import VentanaLogin


class VentanaPresentacion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(1000, 700)  # Aumentado considerablemente

        # Logo
        self.logo = QLabel(self)
        ruta_logo = obtener_ruta_absoluta("img/logo.jpg")
        pixmap = QPixmap(ruta_logo)
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
        # Comienza desde el centro exacto
        self.logo.setGeometry(500, 350, 0, 0)

        # Animación
        self.animacion = QPropertyAnimation(self.logo, b"geometry")
        self.animacion.setDuration(1500)
        self.animacion.setStartValue(QRect(500, 350, 0, 0))
        # Totalmente visible dentro de 1000x700
        self.animacion.setEndValue(QRect(150, 117, 700, 466))
        self.animacion.finished.connect(self.esperar_y_cambiar)

        self.animacion.start()

    def esperar_y_cambiar(self):
        QTimer.singleShot(30, self.mostrar_login)

    def mostrar_login(self):
        self.login = VentanaPresentacion()
        self.login.show()
        self.close()
