from PySide6.QtCore import QThread, Signal
from modelos.recepcionamiento_consultas import obtener_datos_completos_recepcionamiento


class HiloCargaRecepcionamiento(QThread):
    senal_datos_cargados = Signal(dict)

    def run(self):
        try:
            print("📦 Cargando datos en segundo plano...")
            datos = obtener_datos_completos_recepcionamiento()
            print("📦 Datos listos, emitiendo señal...")
            self.senal_datos_cargados.emit(datos)
        except Exception as e:
            print(f"❌ Error en hilo de carga de recepcionamiento: {e}")
