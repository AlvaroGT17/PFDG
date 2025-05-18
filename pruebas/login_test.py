"""
Script de prueba manual para la ventana de inicio de sesión (`VentanaLogin`).

Este módulo permite abrir `VentanaLogin` de forma independiente, útil para probar
visualmente la interfaz, estilos, comportamiento del cierre, validación de campos, etc.

Puede utilizarse también como función auxiliar en tests automatizados.

Uso desde terminal:
    python -m pruebas.login_test
"""

import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_login import VentanaLogin


def iniciar_ventana_login():
    """
    Crea y retorna una instancia de VentanaLogin para pruebas manuales.

    Returns:
        VentanaLogin: Instancia mostrada de la ventana de login.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    ventana = VentanaLogin()
    ventana.show()
    return ventana


if __name__ == "__main__":
    ventana = iniciar_ventana_login()
    sys.exit(QApplication.instance().exec())
