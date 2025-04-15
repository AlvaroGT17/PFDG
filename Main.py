import os
import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_presentacion import VentanaPresentacion
from controladores.login_controlador import LoginControlador
from controladores.recuperar_controlador import RecuperarControlador
from controladores.inicio_controlador import InicioControlador


class Aplicacion:
    def __init__(self):
        os.environ["G_MESSAGES_DEBUG"] = "none"
        self.app = QApplication(sys.argv)

        # Ventana de presentación
        self.ventana_presentacion = VentanaPresentacion()
        self.ventana_presentacion.mostrar_login = self.mostrar_login
        self.ventana_presentacion.show()

        # Inicializar controladores como None
        self.controlador_login = None
        self.controlador_recuperar = None

    def mostrar_login(self):
        # Cerrar presentación si sigue abierta
        self.ventana_presentacion.close()

        # Mostrar ventana de login con su controlador
        self.controlador_login = LoginControlador()
        self.controlador_login.senal_abrir_recuperacion.connect(
            self.mostrar_recuperar)
        self.controlador_login.senal_login_exitoso.connect(
            self.mostrar_dashboard)
        self.controlador_login.mostrar()

    def mostrar_recuperar(self):
        if self.controlador_login:
            self.controlador_login.cerrar()

        self.controlador_recuperar = RecuperarControlador()
        self.controlador_recuperar.senal_volver_login.connect(
            self.mostrar_login)
        self.controlador_recuperar.mostrar()

    def mostrar_dashboard(self, usuario):
        self.controlador_inicio = InicioControlador(
            usuario["nombre"], usuario["rol"])
        self.controlador_inicio.senal_cerrar_sesion.connect(self.mostrar_login)
        self.controlador_inicio.mostrar()

    def ejecutar(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    aplicacion = Aplicacion()
    aplicacion.ejecutar()
