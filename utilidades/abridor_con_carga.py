"""
Módulo que define la clase `AbridorConCarga`, utilizada para mostrar una ventana con animación de carga
(GIF) mientras se ejecuta una operación pesada en segundo plano mediante hilos.

Una vez completada la carga, se instancia la ventana de destino y su controlador con los datos cargados.
"""

from PySide6.QtCore import QTimer
from vistas.ventana_carga_gif import VentanaCargaGif
from utilidades.hilos.hilo_generico import HiloGenericoCarga


class AbridorConCarga:
    """
    Controlador de utilidad para abrir ventanas que requieren tiempo de carga previo.

    Esta clase muestra una animación de carga (ventana con GIF) mientras se ejecuta una función
    que obtiene los datos necesarios en segundo plano. Una vez finalizada la carga, se crea la
    ventana final y se le asigna su controlador correspondiente.

    Ideal para vistas que necesitan precargar datos desde base de datos o cálculos pesados.
    """

    def __init__(self, ventana_padre, clase_ventana, clase_controlador, funcion_carga):
        """
        Inicializa el flujo de carga con animación y lanza el hilo de carga de datos.

        Args:
            ventana_padre (QWidget): La ventana que actúa como padre de la animación de carga.
            clase_ventana (type): Clase de la ventana que se abrirá tras la carga.
            clase_controlador (type): Clase del controlador asociado a la ventana.
            funcion_carga (function): Función que se ejecutará en segundo plano para obtener los datos.
        """
        self.ventana_padre = ventana_padre
        self.clase_ventana = clase_ventana
        self.clase_controlador = clase_controlador
        self.funcion_carga = funcion_carga

        # Mostrar GIF de carga
        self.ventana_carga = VentanaCargaGif()
        self.ventana_carga.mostrar(self.ventana_padre)

        # Crear y lanzar el hilo
        self.hilo = HiloGenericoCarga(self.funcion_carga)
        self.hilo.senal_datos_cargados.connect(self.continuar)
        self.hilo.finished.connect(self.hilo.deleteLater)
        self.hilo.start()

    def continuar(self, datos):
        """
        Método que se ejecuta automáticamente al completarse el hilo.

        Instancia la nueva ventana y su controlador con los datos recibidos, cierra el GIF
        de carga y lanza la ventana de forma modal.

        Args:
            datos (Any): Datos devueltos por `funcion_carga`.
        """
        self.ventana = self.clase_ventana()
        self.controlador = self.clase_controlador(self.ventana, datos)

        self.ventana_carga.cerrar()

        # Cerrar hilo correctamente
        self.hilo.quit()
        self.hilo.wait()

        QTimer.singleShot(100, self.ventana.exec)
