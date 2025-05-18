"""
Script manual para lanzar la ventana de historial de fichajes.

Este archivo permite abrir visualmente `HistorialControlador` con un usuario
específico, para comprobar el funcionamiento, diseño y datos mostrados
en la ventana de historial.


Uso:
    python -m pruebas.historial_test
"""

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
