# historial_test.py
# ──────────────────────────────
# Lanzador manual para abrir la ventana de historial de fichajes.
# Este archivo NO debe incluir funciones de test.
# Para pruebas automáticas, usar: test_historial.py

import sys
from PySide6.QtWidgets import QApplication
from controladores.historial_controlador import HistorialControlador

if __name__ == "__main__":
    app = QApplication(sys.argv)

    usuario_id = 1
    es_admin = False

    controlador = HistorialControlador(usuario_id, es_admin)
    controlador.mostrar()

    sys.exit(app.exec())
