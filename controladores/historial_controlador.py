from PySide6.QtCore import QObject
from vistas.ventana_historial import VentanaHistorial
from modelos.historial_consultas import (
    obtener_fichajes_personales,
    obtener_fichajes_globales
)


class HistorialControlador(QObject):
    def __init__(self, usuario_id, es_admin=False):
        super().__init__()
        self.usuario_id = usuario_id
        self.es_admin = es_admin
        self.ventana = VentanaHistorial(es_admin=es_admin)
        self.cargar_datos()

    def mostrar(self):
        self.ventana.show()

    def cargar_datos(self):
        if self.es_admin:
            fichajes = obtener_fichajes_globales()
        else:
            fichajes = obtener_fichajes_personales(self.usuario_id)

        self.ventana.cargar_datos(fichajes)
