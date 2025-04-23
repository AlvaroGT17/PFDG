from PySide6.QtWidgets import QApplication
from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    correo_defecto = "cliente@ejemplo.com"
    ventana = VentanaCorreoConfirmacion(correo_defecto)
    resultado = ventana.exec()

    if resultado == VentanaCorreoConfirmacion.Accepted:
        if ventana.correo_seleccionado == "DEFECTO":
            print(f"📧 Se enviará al correo por defecto: {correo_defecto}")
        else:
            print(
                f"📧 Se enviará al correo personalizado: {ventana.correo_seleccionado}")
    else:
        print("❌ Envío cancelado por el usuario.")

    sys.exit()

# # para ejecutar el test, usar el siguiente comando en la terminal:
# # python -m pruebas.correoConfirmacion_test
