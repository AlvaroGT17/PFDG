from PySide6.QtCore import QObject, Signal
from vistas.ventana_inicio import VentanaInicio


class InicioControlador(QObject):
    senal_cerrar_sesion = Signal()

    def __init__(self, nombre, rol):
        super().__init__()
        self.ventana = VentanaInicio(nombre, rol)

        # 🔧 Conectar botón de cerrar sesión usando clave en minúsculas
        if "cerrar sesión" in self.ventana.botones:
            self.ventana.botones["cerrar sesión"].clicked.connect(self.cerrar)

    def mostrar(self):
        self.ventana.show()

    def cerrar(self):
        self.ventana.close()
        self.senal_cerrar_sesion.emit()
