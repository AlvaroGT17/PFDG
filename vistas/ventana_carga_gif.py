"""
Módulo para la ventana de carga animada con GIF en el sistema ReyBoxes.

Esta ventana modal se utiliza para mostrar visualmente que se está ejecutando
una operación en segundo plano, como la carga de datos, generación de informes
o procesos largos. Es una interfaz sin bordes, centrada y con fondo transparente.
"""

from PySide6.QtGui import QIcon, QMovie
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QApplication
from utilidades.rutas import obtener_ruta_absoluta


class VentanaCargaGif(QDialog):
    """
    Ventana modal que muestra un GIF animado de carga centrado en pantalla.

    Se utiliza para indicar visualmente procesos en ejecución como carga de datos,
    generación de informes o procesamiento prolongado. Es transparente, sin bordes
    y siempre visible sobre el resto de la interfaz.

    Atributos:
        label_gif (QLabel): Etiqueta que contiene el GIF animado.
        movie (QMovie): Objeto que controla la reproducción del GIF.
    """

    def __init__(self):
        """
        Inicializa la ventana de carga con atributos de transparencia y sin bordes.

        Configura el layout con un `QLabel` que reproduce un GIF animado.
        """
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

        Inicia la animación del GIF y ajusta el tamaño de la ventana.

        Args:
            ventana_padre (QWidget, optional): Ventana sobre la que se centrará el diálogo.
                                               Si no se especifica, se centra en la pantalla principal.
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
        Detiene la animación del GIF y cierra la ventana de carga.
        """
        self.movie.stop()
        self.close()
