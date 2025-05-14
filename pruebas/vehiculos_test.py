"""
Módulo de prueba para lanzar la ventana de gestión de vehículos (VentanaVehiculos).

Se puede ejecutar desde consola o importar para usar en pruebas automáticas o interactivas.
"""

import sys
from vistas.ventana_vehiculos import VentanaVehiculos

# Marcar si estamos ejecutando como test (esto se sobreescribe desde conftest.py)
setattr(sys, '_called_from_test', False)


def iniciar_ventana_vehiculos():
    """
    Devuelve una instancia de la ventana de vehículos sin mostrarla.

    Returns:
        VentanaVehiculos: instancia de la ventana.
    """
    return VentanaVehiculos()


# Solo ejecuta si es script directo y no estamos en test
if __name__ == "__main__" and not getattr(sys, "_called_from_test", False):
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = iniciar_ventana_vehiculos()
    ventana.show()
    sys.exit(app.exec())
