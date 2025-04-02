from PySide6.QtCore import QObject
from vistas.ventana_fichar import VentanaFichar
from modelos.fichajes_consultas import registrar_fichaje


class FicharControlador(QObject):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.ventana = VentanaFichar()

        self.ventana.btn_confirmar.clicked.connect(self.fichar)

    def mostrar(self):
        self.ventana.show()

    def fichar(self):
        tipo = self.ventana.obtener_tipo_fichaje()
        if not tipo:
            self.ventana.mostrar_error(
                "Debes seleccionar 'Entrada' o 'Salida'")
            return

        registrar_fichaje(self.usuario["id"], tipo)
        self.ventana.mostrar_confirmacion(
            f"Fichaje de {tipo} registrado correctamente.")
        self.ventana.close()
