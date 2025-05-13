"""
Módulo que define un hilo genérico (`HiloGenericoCarga`) para ejecutar funciones de carga en segundo plano.

Está diseñado para ser reutilizado en cualquier parte de la aplicación donde se necesite
cargar datos sin bloquear la interfaz gráfica.
"""

from PySide6.QtCore import QThread, Signal


class HiloGenericoCarga(QThread):
    """
    Hilo genérico reutilizable para ejecutar funciones de carga de datos en segundo plano.

    Emite una señal con los datos una vez completada la ejecución. Se utiliza junto con ventanas
    que requieren operaciones costosas (como consultas a base de datos) para evitar congelar la UI.
    """

    senal_datos_cargados = Signal(object)
    """Señal emitida al terminar el hilo, con los datos devueltos por `funcion_carga`."""

    def __init__(self, funcion_carga):
        """
        Inicializa el hilo con una función que será ejecutada al iniciarse el hilo.

        Args:
            funcion_carga (Callable): Función que se ejecutará en segundo plano para obtener los datos.
        """
        super().__init__()
        self.funcion_carga = funcion_carga

    def run(self):
        """
        Método principal del hilo. Ejecuta la función de carga y emite los datos obtenidos.

        Este método se ejecuta automáticamente cuando se llama a `start()`.
        """
        datos = self.funcion_carga()
        self.senal_datos_cargados.emit(datos)
