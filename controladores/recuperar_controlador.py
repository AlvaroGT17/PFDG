import re
import random
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox

from vistas.ventana_recuperar import VentanaRecuperar
from modelos.login_consultas import (
    obtener_usuario_por_email,
    guardar_codigo_recuperacion
)
from utilidades.correo import enviar_correo
from controladores.verificar_controlador import VerificarControlador


class RecuperarControlador(QObject):
    senal_volver_login = Signal()

    def __init__(self):
        super().__init__()
        self.ventana = VentanaRecuperar()

        # Conexión de eventos
        self.ventana.btn_volver.clicked.connect(self.volver)
        self.ventana.btn_enviar.clicked.connect(self.enviar_codigo)
        self.ventana.input_correo.textChanged.connect(self.validar_correo)
        self.ventana.closeEvent = self.handle_cierre_ventana

    def mostrar(self):
        self.ventana.show()

    def cerrar(self):
        self.ventana.close()

    def volver(self):
        self.cerrar()
        self.senal_volver_login.emit()

    def handle_cierre_ventana(self, event):
        self.senal_volver_login.emit()
        event.accept()

    def validar_correo(self):
        texto = self.ventana.input_correo.text()
        es_valido = re.match(r"[^@]+@[^@]+\.[^@]+", texto)
        self.ventana.btn_enviar.setEnabled(bool(es_valido))

    def enviar_codigo(self):
        correo = self.ventana.input_correo.text().strip()

        if not correo:
            QMessageBox.warning(self.ventana, "Campo requerido",
                                "Por favor introduce tu correo.")
            return

        usuario = obtener_usuario_por_email(correo)
        if not usuario:
            QMessageBox.warning(self.ventana, "Correo no válido",
                                "❌ No se encontró un usuario con ese correo.")
            return

        codigo = str(random.randint(100000, 999999))

        if guardar_codigo_recuperacion(usuario["id"], codigo):
            try:
                enviar_correo(correo, usuario["nombre"], codigo)
                QMessageBox.information(
                    self.ventana,
                    "Código enviado",
                    f"📧 Se ha enviado un código de recuperación a {correo}"
                )
                self.ventana.hide()
                self.controlador_verificacion = VerificarControlador(correo)
                self.controlador_verificacion.senal_volver_recuperar.connect(
                    self.mostrar_otra_vez)
                self.controlador_verificacion.mostrar()

            except Exception as e:
                print("❌ Error al enviar correo:", e)
                QMessageBox.critical(
                    self.ventana,
                    "Error de correo",
                    "❌ No se pudo enviar el correo. Revisa la configuración.")
        else:
            QMessageBox.warning(self.ventana, "Error",
                                "❌ No se pudo guardar el código de recuperación.")

    def mostrar_otra_vez(self):
        self.ventana.show()
