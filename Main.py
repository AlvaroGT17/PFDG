from PySide6.QtWidgets import QApplication
import sys
from vistas.ventana_presentacion import VentanaPresentacion

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = VentanaPresentacion()
    ventana.show()

    sys.exit(app.exec())
