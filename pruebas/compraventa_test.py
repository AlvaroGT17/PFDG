import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_compraventa import VentanaCompraventa

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Pasamos None como ventana_anterior
    ventana_dummy = VentanaCompraventa(None)
    ventana_dummy.show()
    sys.exit(app.exec())

    # Aquí puedes agregar pruebas unitarias o de integración para la ventana de compra-venta para abrir la ventana ejecuta en la consola:
    # python -m pruebas.compraventa_test
