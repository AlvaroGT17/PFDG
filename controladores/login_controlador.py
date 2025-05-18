"""
Controlador del proceso de inicio de sesión de usuarios.

Este módulo permite:
- Mostrar la interfaz de login.
- Validar las credenciales ingresadas.
- Mostrar una ventana de carga durante la verificación.
- Enviar señales al resto de la aplicación al iniciar sesión o solicitar recuperación.

Utiliza:
- `VentanaLogin` para la interfaz de entrada.
- `VentanaCargaGif` para mostrar la animación durante el proceso.
- `obtener_usuario_por_nombre` y `verificar_contrasena` para validación contra la base de datos.
"""
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal, QObject, QTimer
from vistas.ventana_login import VentanaLogin
from modelos.login_consultas import obtener_usuario_por_nombre, verificar_contrasena
from vistas.ventana_carga_gif import VentanaCargaGif


class LoginControlador(QObject):
    """
    Controlador encargado de gestionar el inicio de sesión del usuario.

    Señales:
        senal_abrir_recuperacion: Emitida cuando el usuario solicita recuperar la cuenta.
        senal_login_exitoso: Emitida con un diccionario de usuario si el login es exitoso.
    """
    senal_abrir_recuperacion = Signal()
    senal_login_exitoso = Signal(dict)

    def __init__(self):
        """
        Inicializa el controlador de login y conecta los eventos de la interfaz.
        """
        super().__init__()
        self.ventana = VentanaLogin()
        self.ventana_carga = None  # 👈 ventana de carga vacía al inicio

        self.ventana.btn_entrar.clicked.connect(self.iniciar_proceso_login)
        self.ventana.enlace_recuperar.linkActivated.connect(
            self.abrir_recuperacion)
        self.ventana.input_usuario.returnPressed.connect(
            self.iniciar_proceso_login)
        self.ventana.input_contrasena.returnPressed.connect(
            self.iniciar_proceso_login)
        self.ventana.btn_entrar.setDefault(True)

    def mostrar(self):
        """
        Muestra la ventana de inicio de sesión.
        """
        self.ventana.show()

    def cerrar(self):
        """
        Cierra la ventana de login autorizando su cierre.
        """
        self.ventana.cierre_autorizado = True
        self.ventana.close()

    def abrir_recuperacion(self):
        """
        Cierra la ventana de login y emite la señal para abrir la recuperación de cuenta.
        """
        self.senal_abrir_recuperacion.emit()
        self.cerrar()

    def iniciar_proceso_login(self):
        """
        Inicia el proceso de verificación del login:
        - Verifica que los campos estén completos.
        - Muestra animación de carga.
        - Ejecuta la validación tras un breve retardo.
        """
        nombre = self.ventana.input_usuario.text().strip()
        contrasena = self.ventana.input_contrasena.text()

        errores = []
        if not nombre:
            errores.append("• Falta el nombre de usuario")
        if not contrasena:
            errores.append("• Falta la contraseña")

        if errores:
            QMessageBox.warning(
                self.ventana,
                "Campos incompletos",
                "\n".join(errores),
                QMessageBox.StandardButton.Ok
            )
            return

        # Mostrar ventana de carga
        self.ventana_carga = VentanaCargaGif()
        self.ventana_carga.show()

        # Esperar 200ms para que la animación se vea y luego validar
        QTimer.singleShot(200, lambda: self.validar_login(nombre, contrasena))

    def validar_login(self, nombre, contrasena):
        """
        Verifica el nombre de usuario y contraseña contra la base de datos.
        Muestra un mensaje si es exitoso o si ocurre un error.

        Args:
            nombre (str): Nombre de usuario ingresado.
            contrasena (str): Contraseña ingresada.
        """
        usuario = obtener_usuario_por_nombre(nombre)
        if usuario and verificar_contrasena(contrasena, usuario["password"]):
            self.ventana_carga.cerrar()  # ✅ Cierra video de carga
            QMessageBox.information(
                self.ventana,
                " Login exitoso 👍",
                f"Bienvenido/a, {usuario['nombre']}",
                QMessageBox.StandardButton.Ok
            )
            self.senal_login_exitoso.emit(usuario)
            self.cerrar()
        else:
            self.ventana_carga.cerrar()  # ❌ También cerramos si falla
            QMessageBox.critical(
                self.ventana,
                "❌ Error de autenticación",
                "Nombre o contraseña incorrectos.",
                QMessageBox.StandardButton.Ok
            )
