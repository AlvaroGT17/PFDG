"""
Controlador para la recuperación de contraseña por correo electrónico.

Este controlador permite al usuario:
- Introducir su dirección de correo.
- Validar su existencia en la base de datos.
- Recibir un código temporal de recuperación.
- Continuar con el flujo de verificación si el correo es válido.

Utiliza:
- `VentanaRecuperar`: interfaz gráfica del formulario.
- `VerificarControlador`: controlador para introducir y verificar el código recibido.
- `enviar_correo`: utilidad que envía el código de recuperación al usuario.
"""
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
    """
    Controlador que gestiona la lógica de la pantalla de recuperación de contraseña.

    Señales:
        senal_volver_login: Se emite cuando el usuario desea volver a la pantalla de inicio de sesión.
    """
    senal_volver_login = Signal()

    def __init__(self):
        """
        Inicializa la ventana de recuperación, conecta señales y prepara el flujo.
        """
        super().__init__()
        self.ventana = VentanaRecuperar()

        # Conexión de eventos
        self.ventana.btn_volver.clicked.connect(self.volver)
        self.ventana.btn_enviar.clicked.connect(self.enviar_codigo)
        self.ventana.input_correo.textChanged.connect(self.validar_correo)
        self.ventana.closeEvent = self.handle_cierre_ventana

    def mostrar(self):
        """Muestra la ventana de recuperación."""
        self.ventana.show()

    def cerrar(self):
        """Cierra la ventana de recuperación."""
        self.ventana.close()

    def volver(self):
        """Vuelve al login, emitiendo la señal correspondiente."""
        self.cerrar()
        self.senal_volver_login.emit()

    def handle_cierre_ventana(self, event):
        """
        Manejador del cierre de ventana por el aspa (❌).

        Args:
            event (QCloseEvent): Evento de cierre.
        """
        self.senal_volver_login.emit()
        event.accept()

    def validar_correo(self):
        """
        Habilita o deshabilita el botón de envío en función de si el correo introducido
        cumple con un formato básico válido.
        """
        texto = self.ventana.input_correo.text()
        es_valido = re.match(r"[^@]+@[^@]+\.[^@]+", texto)
        self.ventana.btn_enviar.setEnabled(bool(es_valido))

    def enviar_codigo(self):
        """
        Verifica si el correo pertenece a un usuario registrado.
        Si es así, genera un código de recuperación, lo guarda en base de datos,
        y lo envía por correo. Después lanza la ventana de verificación.
        """
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
        """
        Muestra nuevamente la ventana de recuperación después de regresar
        desde la pantalla de verificación.
        """
        self.ventana.show()
