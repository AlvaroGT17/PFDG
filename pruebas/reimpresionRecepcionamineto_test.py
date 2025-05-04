#!/usr/bin/env python3
# reimpresionRecepcionamineto_test.py
# ──────────────────────────────────
# Script de prueba autónomo para abrir la ventana de reimpresión
# de recepcionamientos sin arrancar todo el programa principal.

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from vistas.ventana_reimpresionRecepcionamiento import VentanaReimpresionRecepcionamiento

# --- Ajusta el import si el módulo está en otra carpeta -----------------
# Añadimos el directorio actual al sys.path para facilitar el import
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Importamos la ventana a testear


def main() -> None:
    """Crea la aplicación Qt y muestra la ventana de reimpresión."""
    app = QApplication(sys.argv)

    # Instancia de la ventana (usa datos de ejemplo si no se pasa lista)
    dlg = VentanaReimpresionRecepcionamiento()
    dlg.show()

    # Ejecutamos el bucle de eventos
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# para ejecutar el test, usa el siguiente comando en la terminal:
# python -m pruebas.reimpresionRecepcionamineto_test
