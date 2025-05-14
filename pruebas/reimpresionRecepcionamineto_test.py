#!/usr/bin/env python3
# reimpresionRecepcionamineto_test.py
# ───────────────────────────────────
# Script de prueba autónomo para abrir la ventana de reimpresión
# de recepcionamientos sin arrancar todo el programa principal.

"""
TEST MANUAL: Ventana de reimpresión de recepcionamientos

Este script permite abrir de forma aislada la ventana `VentanaReimpresionRecepcionamiento`
para pruebas visuales, sin necesidad de ejecutar toda la aplicación principal.

Es útil para desarrolladores que desean comprobar estilos, disposición visual,
funcionalidad básica de carga y comportamiento general de esta pantalla específica.

Se puede ejecutar directamente con:
    python -m pruebas.reimpresionRecepcionamineto_test
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from vistas.ventana_reimpresionRecepcionamiento import VentanaReimpresionRecepcionamiento

# ------------------------------------------------------------------------------
# GARANTÍA DE IMPORTACIÓN: Asegura que se pueda ejecutar directamente
# desde terminal sin problemas con rutas relativas
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ------------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL: Lanza la ventana de reimpresión
# ------------------------------------------------------------------------------


def main() -> None:
    """
    Crea la aplicación Qt y muestra la ventana de reimpresión de recepcionamientos.

    Se usa para testeo visual o funcional durante el desarrollo.
    """
    app = QApplication(sys.argv)

    # Cargar la ventana sin parámetros adicionales
    dlg = VentanaReimpresionRecepcionamiento()
    dlg.show()

    # Ejecutamos el bucle de eventos Qt
    sys.exit(app.exec())


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

# Nota:
# Para ejecutar este test, usa el siguiente comando desde la raíz del proyecto:
#    python -m pruebas.reimpresionRecepcionamineto_test
