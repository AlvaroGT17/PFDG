from PySide6.QtWidgets import QApplication
import sys
from vistas.ventana_login import VentanaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec())
