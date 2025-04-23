import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_presupuesto import VentanaPresupuesto

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = VentanaPresupuesto()
    ventana.exec()  # Modal (bloquea hasta cerrar)

    sys.exit()

# Para ejecutar el test, usa el siguiente comando en la terminal:
# python -m pruebas.presupuesto_test
