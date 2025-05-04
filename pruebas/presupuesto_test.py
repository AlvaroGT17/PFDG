import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_presupuesto import VentanaPresupuesto
from controladores.presupuesto_controlador import PresupuestoControlador

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = VentanaPresupuesto()
    PresupuestoControlador(ventana)
    ventana.exec()  # Modal (bloquea hasta cerrar)

    sys.exit()

# Para ejecutar el test, usa el siguiente comando en la terminal:
# python -m pruebas.presupuesto_test
