import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_anadirTareaPresupuesto import DialogoTarea

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogo = DialogoTarea()

    if dialogo.exec():
        datos = dialogo.obtener_datos()
        if datos:
            tarea, horas, precio, total = datos
            print("Tarea:", tarea)
            print("Horas:", horas)
            print("Precio/hora:", precio)
            print("Total:", total)
        else:
            print("❌ Error: Datos inválidos.")
    else:
        print("❌ Cancelado por el usuario.")

    sys.exit()

# Para ejecutar el test, usa el siguiente comando en la terminal:
# python -m pruebas.anadirTareaPresupuesto_test
