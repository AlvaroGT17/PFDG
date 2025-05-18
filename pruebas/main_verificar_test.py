"""
Script manual para probar la ventana de verificación de código.

Este archivo permite lanzar `VerificarControlador` con un correo de prueba
previamente registrado, lo que facilita el testeo visual y funcional de la
pantalla de verificación de código OTP, sin depender del flujo completo de la app.

Uso recomendado:
    python -m pruebas.verificar_test
"""

import sys
from PySide6.QtWidgets import QApplication
from controladores.verificar_controlador import VerificarControlador


def iniciar_controlador_verificacion():
    """
    Devuelve una instancia del controlador de verificación con correo de prueba.

    Returns:
        VerificarControlador: Controlador listo para ser mostrado en tests visuales.
    """
    email_de_prueba = "cresnik17021983@gmail.com"
    return VerificarControlador(email_de_prueba)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    controlador = iniciar_controlador_verificacion()
    controlador.mostrar()

    sys.exit(app.exec())
