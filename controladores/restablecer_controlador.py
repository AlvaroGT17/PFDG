"""
Controlador para la ventana de restablecimiento de contraseña.

Gestiona:
- La verificación de coincidencia entre la nueva contraseña y su confirmación.
- La actualización de la contraseña en la base de datos.
- El cierre correcto de la ventana y retorno al login tras una acción exitosa o cancelación.

Utiliza la vista `VentanaRestaurar` y la función `actualizar_contrasena` del modelo.
"""

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox, QApplication
from vistas.ventana_restaurar import VentanaRestaurar
from modelos.login_consultas import actualizar_contrasena


class RestablecerControlador(QObject):
    """
    Controlador que gestiona la lógica de la ventana para restablecer una contraseña.

    Señales:
        senal_volver_login: Emitida para regresar al login tras restablecer o cancelar.

    Métodos:
        mostrar(): Muestra la ventana.
        cerrar(): Cierra la ventana.
        volver(): Emite señal y cierra la ventana (botón "Volver").
        cerrar_ventana(event): Emite señal y acepta el cierre por aspa.
        restablecer(): Verifica y guarda la nueva contraseña, mostrando mensajes al usuario.
    """

    senal_volver_login = Signal()

    def __init__(self, email):
        """
        Inicializa la ventana y conecta sus botones con la lógica correspondiente.

        Args:
            email (str): Correo del usuario que va a restablecer su contraseña.
        """
        super().__init__()
        self.email = email
        self.ventana = VentanaRestaurar()

        # Conexiones de botones
        self.ventana.btn_volver.clicked.connect(self.volver)
        self.ventana.btn_guardar.clicked.connect(self.restablecer)
        self.ventana.closeEvent = self.cerrar_ventana

    def mostrar(self):
        """
        Muestra la ventana de restablecimiento de contraseña.
        """
        self.ventana.show()

    def cerrar(self):
        """
        Cierra la ventana actual.
        """
        self.ventana.close()

    def volver(self):
        """
        Acción del botón "Volver": cierra la ventana y emite señal para regresar al login.
        """
        self.cerrar()
        self.senal_volver_login.emit()

    def cerrar_ventana(self, event):
        """
        Maneja el cierre de la ventana desde el botón de cerrar (❌).

        Args:
            event (QCloseEvent): Evento de cierre.
        """
        self.senal_volver_login.emit()
        event.accept()

    def restablecer(self):
        """
        Verifica que los campos de nueva contraseña coincidan y no estén vacíos.

        Si todo es correcto, actualiza la contraseña usando el modelo.
        Muestra mensajes según el resultado y cierra todas las ventanas si tiene éxito.
        """
        nueva = self.ventana.input_nueva.text().strip()
        repetir = self.ventana.input_repetir.text().strip()

        if not nueva or not repetir:
            QMessageBox.warning(self.ventana, "Campos incompletos",
                                "Por favor completa ambos campos.")
            return

        if nueva != repetir:
            QMessageBox.warning(self.ventana, "No coinciden",
                                "Las contraseñas no coinciden.")
            return

        if actualizar_contrasena(self.email, nueva):
            QMessageBox.information(self.ventana, "Contraseña actualizada",
                                    "✅ Tu contraseña se ha actualizado correctamente.")
            # Cerrar todas las ventanas abiertas
            for widget in QApplication.topLevelWidgets():
                widget.close()
            self.senal_volver_login.emit()
        else:
            QMessageBox.critical(self.ventana, "Error",
                                 "❌ No se pudo actualizar la contraseña.")
