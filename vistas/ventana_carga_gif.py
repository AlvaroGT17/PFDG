from PySide6.QtGui import QIcon, QMovie
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QApplication
from utilidades.rutas import obtener_ruta_absoluta


class VentanaCargaGif(QDialog):
    """
    Ventana modal que muestra un GIF animado de carga centrado en pantalla.

    Se utiliza para indicar visualmente procesos en ejecución como carga de datos,
    generación de informes, o procesamiento prolongado.
    """

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
        """
        Muestra la ventana de carga centrada en pantalla o sobre una ventana padre.

        Parámetros:
            ventana_padre (QWidget): Ventana sobre la que se centrará el diálogo (opcional).
        """
        self.movie.start()
        self.adjustSize()
        if ventana_padre:
            center = ventana_padre.frameGeometry().center()
        else:
            center = QApplication.primaryScreen().availableGeometry().center()
        self.move(center - self.rect().center())
        self.show()

    def cerrar(self):
        """
        Detiene la animación y cierra la ventana.
        """
        self.movie.stop()
        self.close()
