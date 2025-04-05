# pruebas/vehiculos_test.py
import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_vehiculos import VentanaVehiculos

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = VentanaVehiculos()
    ventana.show()

    sys.exit(app.exec())

# Para ejecutarlo desde la terminal: ---- python -m pruebas.vehiculos_test ------
