import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_login import VentanaLogin


def iniciar_ventana_login():
    """
    Crea y retorna una instancia de VentanaLogin para pruebas manuales.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    ventana = VentanaLogin()
    ventana.show()
    return ventana


if __name__ == "__main__":
    ventana = iniciar_ventana_login()
    sys.exit(QApplication.instance().exec())
