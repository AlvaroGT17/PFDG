from PySide6.QtCore import QObject, Signal
from vistas.ventana_inicio import VentanaInicio


class InicioControlador(QObject):
    senal_cerrar_sesion = Signal()

    def __init__(self, nombre, rol):
        super().__init__()
        self.ventana = VentanaInicio(nombre, rol)

        self.ventana.botones["Cerrar sesión"].clicked.connect(
            self.cerrar_sesion)

    def mostrar(self):
        self.ventana.show()

    def cerrar(self):
        self.ventana.close()

    def cerrar_sesion(self):
        self.cerrar()
        self.senal_cerrar_sesion.emit()
