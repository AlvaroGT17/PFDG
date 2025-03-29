import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_verificar import VentanaVerificar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaVerificar()
    ventana.show()
    sys.exit(app.exec())
