"""
Módulo principal de la aplicación ReyBoxes.

Este archivo contiene la clase `Aplicacion`, encargada de iniciar la aplicación,
mostrar la ventana de presentación y gestionar la transición entre las distintas
ventanas principales: login, recuperación de cuenta y panel de inicio (dashboard).

Se sigue el patrón MVC, separando claramente la lógica de controladores y vistas.
"""

import os
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from controladores.login_controlador import LoginControlador
from controladores.recuperar_controlador import RecuperarControlador
from controladores.inicio_controlador import InicioControlador
from vistas.ventana_presentacion import VentanaPresentacion
from utilidades.rutas import obtener_ruta_absoluta


class Aplicacion:
    """
    Clase principal que gestiona el ciclo de vida de la aplicación.

    Se encarga de iniciar la interfaz gráfica, mostrar la ventana de presentación
    y manejar los cambios entre login, recuperación de cuenta y el dashboard principal.
    """

    def __init__(self):
        """
        Inicializa la aplicación.

        - Crea la instancia de QApplication.
        - Establece el icono principal.
        - Muestra la ventana de presentación.
        """
        os.environ["G_MESSAGES_DEBUG"] = "none"
        self.app = QApplication(sys.argv)

        self.app.setWindowIcon(QIcon(obtener_ruta_absoluta("img/favicon.ico")))

        # Ventana de presentación
        self.ventana_presentacion = VentanaPresentacion()
        self.ventana_presentacion.mostrar_login = self.mostrar_login
        self.ventana_presentacion.show()

        # Inicializar controladores como None
        self.controlador_login = None
        self.controlador_recuperar = None

    def mostrar_login(self):
        """
        Muestra la ventana de inicio de sesión.

        - Cierra la ventana de presentación si aún está abierta.
        - Crea y muestra el controlador del login.
        - Conecta señales para navegación a recuperación o dashboard.
        """
        self.ventana_presentacion.close()

        self.controlador_login = LoginControlador()
        self.controlador_login.senal_abrir_recuperacion.connect(
            self.mostrar_recuperar)
        self.controlador_login.senal_login_exitoso.connect(
            self.mostrar_dashboard)
        self.controlador_login.mostrar()

    def mostrar_recuperar(self):
        """
        Muestra la ventana de recuperación de cuenta.

        - Cierra la ventana de login si está abierta.
        - Crea y muestra el controlador de recuperación.
        - Conecta la señal para volver al login.
        """
        if self.controlador_login:
            self.controlador_login.cerrar()

        self.controlador_recuperar = RecuperarControlador()
        self.controlador_recuperar.senal_volver_login.connect(
            self.mostrar_login)
        self.controlador_recuperar.mostrar()

    def mostrar_dashboard(self, usuario):
        """
        Muestra la ventana principal (dashboard) tras un login exitoso.

        :param usuario: Diccionario con los datos del usuario autenticado.
                        Debe contener las claves 'nombre' y 'rol'.
        """
        self.controlador_inicio = InicioControlador(
            usuario["nombre"], usuario["rol"])
        self.controlador_inicio.senal_cerrar_sesion.connect(self.mostrar_login)
        self.controlador_inicio.mostrar()

    def ejecutar(self):
        """
        Ejecuta el bucle principal de la aplicación.
        """
        sys.exit(self.app.exec())


if __name__ == "__main__":
    aplicacion = Aplicacion()
    aplicacion.ejecutar()
