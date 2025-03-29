from PySide6.QtWidgets import QApplication
import sys

from controladores.verificar_controlador import VerificarControlador

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Usa un correo que ya exista en tu base de datos para probar la verificación
    email_de_prueba = "cresnik17021983@gmail.com"

    controlador = VerificarControlador(email_de_prueba)
    controlador.mostrar()

    sys.exit(app.exec())
