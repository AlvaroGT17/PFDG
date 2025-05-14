"""
Script manual para probar la ventana de verificación de código.

Este archivo permite lanzar `VerificarControlador` con un correo de prueba,
ya registrado en la base de datos. Útil para verificar funcionamiento manual.
"""

import sys
from PySide6.QtWidgets import QApplication
from controladores.verificar_controlador import VerificarControlador


def iniciar_controlador_verificacion():
    """
    Devuelve una instancia del controlador de verificación.
    Se utiliza en tests automáticos.
    """
    email_de_prueba = "cresnik17021983@gmail.com"
    return VerificarControlador(email_de_prueba)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    controlador = iniciar_controlador_verificacion()
    controlador.mostrar()

    sys.exit(app.exec())
