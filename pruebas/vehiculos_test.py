"""
Módulo de prueba para lanzar la ventana de gestión de vehículos (`VentanaVehiculos`).

Permite:
- Ejecutar manualmente la ventana desde consola para validaciones visuales.
- Importar la función `iniciar_ventana_vehiculos()` desde tests automatizados o visores interactivos.

Este módulo detecta si está siendo ejecutado como parte de una prueba (mediante `sys._called_from_test`)
y en ese caso no lanza la interfaz gráfica automáticamente.

Forma parte del sistema de desarrollo y pruebas del entorno ReyBoxes.
"""

import sys
from vistas.ventana_vehiculos import VentanaVehiculos

# Marcar si estamos ejecutando como test (se puede sobreescribir desde conftest.py)
setattr(sys, '_called_from_test', False)


def iniciar_ventana_vehiculos():
    """
    Crea y devuelve una instancia de la ventana de gestión de vehículos.

    Esta función está diseñada para:
    - Uso en pruebas visuales o manuales.
    - Integración con visores como `SelectorVentana`.
    - Reutilización en tests automatizados con `pytest`.

    Returns:
        VentanaVehiculos: Instancia de la ventana inicializada (sin mostrar).
    """
    return VentanaVehiculos()


# Solo ejecuta la ventana si se llama desde consola y no desde un test
if __name__ == "__main__" and not getattr(sys, "_called_from_test", False):
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = iniciar_ventana_vehiculos()
    ventana.show()
    sys.exit(app.exec())

# para ejecutar el modulo desde consola:
# python -m pruebas.vehiculos_test
