from PySide6.QtCore import QThread, Signal


class HiloGenericoCarga(QThread):
    senal_datos_cargados = Signal(object)

    def __init__(self, funcion_carga):
        super().__init__()
        self.funcion_carga = funcion_carga

    def run(self):
        datos = self.funcion_carga()
        self.senal_datos_cargados.emit(datos)
