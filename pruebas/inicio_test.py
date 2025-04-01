# pruebas/inicio_test.py
import sys
from PySide6.QtWidgets import QApplication
from controladores.inicio_controlador import InicioControlador

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ⚙️ Usuario simulado para pruebas
    nombre = "CRESNIK"
    rol = "Administrador"

    controlador_inicio = InicioControlador(nombre, rol)
    controlador_inicio.senal_cerrar_sesion.connect(app.quit)
    controlador_inicio.mostrar()

    sys.exit(app.exec())

    # Para ejecutarlo desde la terminal: python -m pruebas.inicio_test
