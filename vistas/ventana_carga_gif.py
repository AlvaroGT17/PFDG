from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QApplication
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt
from utilidades.rutas import obtener_ruta_absoluta


class VentanaCargaGif(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label_gif = QLabel()
        ruta_gif = obtener_ruta_absoluta("img/gif/gifcarga.gif")

        self.movie = QMovie(ruta_gif)
        self.label_gif.setMovie(self.movie)
        self.label_gif.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label_gif)

    def mostrar(self, ventana_padre=None):
        self.movie.start()
        self.adjustSize()
        if ventana_padre:
            center = ventana_padre.frameGeometry().center()
        else:
            center = QApplication.primaryScreen().availableGeometry().center()
        self.move(center - self.rect().center())
        self.show()

    def cerrar(self):
        self.movie.stop()
        self.close()
