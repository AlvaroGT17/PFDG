from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox, QApplication

from vistas.ventana_restaurar import VentanaRestaurar
from modelos.login_consultas import actualizar_contrasena


class RestablecerControlador(QObject):
    senal_volver_login = Signal()

    def __init__(self, email):
        super().__init__()
        self.email = email
        self.ventana = VentanaRestaurar()

        # Conexiones de botones
        self.ventana.btn_volver.clicked.connect(self.volver)
        self.ventana.btn_guardar.clicked.connect(self.restablecer)
        self.ventana.closeEvent = self.cerrar_ventana

    def mostrar(self):
        self.ventana.show()

    def cerrar(self):
        self.ventana.close()

    def volver(self):
        self.cerrar()
        self.senal_volver_login.emit()

    def cerrar_ventana(self, event):
        self.senal_volver_login.emit()
        event.accept()

    def restablecer(self):
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
