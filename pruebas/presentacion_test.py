"""
Script de prueba visual para la ventana de presentación (splash screen).

Este módulo permite lanzar manualmente `VentanaPresentacion` de forma aislada,
para comprobar su animación, transparencia, tamaño o comportamiento al iniciar.

Uso:
    python -m pruebas.presentacion_test
"""

import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_presentacion import VentanaPresentacion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = VentanaPresentacion()
    splash.show()
    sys.exit(app.exec())
