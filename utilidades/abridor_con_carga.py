from PySide6.QtCore import QTimer
from vistas.ventana_carga_gif import VentanaCargaGif
from utilidades.hilos.hilo_generico import HiloGenericoCarga


class AbridorConCarga:
    def __init__(self, ventana_padre, clase_ventana, clase_controlador, funcion_carga):
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
        self.ventana = self.clase_ventana()
        self.controlador = self.clase_controlador(self.ventana, datos)

        self.ventana_carga.cerrar()

        # ⏹️ Cerrar hilo correctamente
        self.hilo.quit()
        self.hilo.wait()

        QTimer.singleShot(100, self.ventana.exec)
