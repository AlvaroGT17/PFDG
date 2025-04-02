import sys
from PySide6.QtWidgets import QApplication
from controladores.fichar_controlador import FicharControlador

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Usuario de prueba simulado
    usuario_ficticio = {
        "id": 6,
        "nombre": "CRESNIK",
        "rol_id": 1
    }

    controlador = FicharControlador(usuario_ficticio)
    controlador.mostrar()

    sys.exit(app.exec())

    # Para ejecutar esta prueba, usa en la consola de comando  ----  python -m pruebas.fichar_test ----
