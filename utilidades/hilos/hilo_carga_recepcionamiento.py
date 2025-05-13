"""
Módulo que define el hilo `HiloCargaRecepcionamiento`, utilizado para cargar datos
completos de recepcionamiento en segundo plano, sin bloquear la interfaz gráfica.

Este hilo utiliza la función `obtener_datos_completos_recepcionamiento` del modelo correspondiente
y emite una señal al completarse con los datos resultantes.
"""

from PySide6.QtCore import QThread, Signal
from modelos.recepcionamiento_consultas import obtener_datos_completos_recepcionamiento


class HiloCargaRecepcionamiento(QThread):
    """
    Hilo específico para cargar los datos del módulo de recepcionamiento en segundo plano.

    Al finalizar la carga, emite una señal con los datos obtenidos en forma de diccionario.
    """

    senal_datos_cargados = Signal(dict)
    """Señal emitida cuando los datos han sido cargados correctamente."""

    def run(self):
        """
        Método que se ejecuta cuando se inicia el hilo.

        Carga los datos de recepcionamiento utilizando el modelo correspondiente
        y emite la señal `senal_datos_cargados` al completarse. Maneja errores con impresión por consola.
        """
        try:
            print("📦 Cargando datos en segundo plano...")
            datos = obtener_datos_completos_recepcionamiento()
            print("📦 Datos listos, emitiendo señal...")
            self.senal_datos_cargados.emit(datos)
        except Exception as e:
            print(f"❌ Error en hilo de carga de recepcionamiento: {e}")
