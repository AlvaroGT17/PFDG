# pruebas/presentacion_test.py
import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_presentacion import VentanaPresentacion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = VentanaPresentacion()
    splash.show()
    sys.exit(app.exec())
