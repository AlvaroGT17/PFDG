from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal, QObject
from vistas.ventana_login import VentanaLogin
from modelos.login_consultas import obtener_usuario_por_nombre, verificar_contrasena


class LoginControlador(QObject):
    senal_abrir_recuperacion = Signal()
    # Emitimos los datos del usuario autenticado
    senal_login_exitoso = Signal(dict)

    def __init__(self):
        super().__init__()
        self.ventana = VentanaLogin()

        # Conectar señales internas de la vista con funciones del controlador
        self.ventana.btn_entrar.clicked.connect(self.verificar_login)
        self.ventana.enlace_recuperar.linkActivated.connect(
            self.abrir_recuperacion)
        # ✅ Permitir login al presionar Enter desde el campo de usuario y contraseña
        self.ventana.input_usuario.returnPressed.connect(self.verificar_login)
        self.ventana.input_contrasena.returnPressed.connect(
            self.verificar_login)

    def mostrar(self):
        self.ventana.show()

    def cerrar(self):
        self.ventana.close()

    def abrir_recuperacion(self):
        self.senal_abrir_recuperacion.emit()
        self.cerrar()

    def verificar_login(self):
        nombre = self.ventana.input_usuario.text().strip()
        contrasena = self.ventana.input_contrasena.text()

        if not nombre or not contrasena:
            QMessageBox.warning(self.ventana, "Campos requeridos",
                                "Por favor completa todos los campos.")
            return

        usuario = obtener_usuario_por_nombre(nombre)
        if usuario and verificar_contrasena(contrasena, usuario["password"]):
            QMessageBox.information(
                self.ventana, "Login exitoso", f"Bienvenido/a, {usuario['nombre']}")
            self.senal_login_exitoso.emit(usuario)
            self.cerrar()
        else:
            QMessageBox.critical(
                self.ventana, "Error de autenticación", "Nombre o contraseña incorrectos.")

    def verificar_login(self):
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

        usuario = obtener_usuario_por_nombre(nombre)
        if usuario and verificar_contrasena(contrasena, usuario["password"]):
            QMessageBox.information(
                self.ventana,
                "✅ Login exitoso",
                f"Bienvenido/a, {usuario['nombre']}",
                QMessageBox.StandardButton.Ok
            )
            self.senal_login_exitoso.emit(usuario)
            self.cerrar()
        else:
            QMessageBox.critical(
                self.ventana,
                "❌ Error de autenticación",
                "Nombre o contraseña incorrectos.",
                QMessageBox.StandardButton.Ok
            )
