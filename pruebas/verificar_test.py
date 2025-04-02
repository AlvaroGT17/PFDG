import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_verificar import VentanaVerificar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaVerificar()
    ventana.show()
    sys.exit(app.exec())

    # Para arrancar la ventana hay que ejecutar el siguiente comando en la consola de comandos:
    # python -m pruebas.verificar_test
