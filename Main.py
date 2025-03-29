import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_presentacion import VentanaPresentacion
from controladores.login_controlador import LoginControlador
from controladores.recuperar_controlador import RecuperarControlador


class Aplicacion:
    def __init__(self):
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
        print(f"🧠 Login correcto: {usuario['nombre']} ({usuario['rol']})")
        # Aquí mostrarías la ventana principal según el rol del usuario

    def ejecutar(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    aplicacion = Aplicacion()
    aplicacion.ejecutar()
