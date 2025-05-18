"""
Módulo de prueba para ejecutar manualmente el diálogo de tareas (`DialogoTarea`) desde consola.

Permite:
- Abrir el formulario de tareas y probar su validación.
- Ver por consola los datos introducidos si el diálogo es aceptado.
- Ver mensajes de error si se cancela o si los datos son inválidos.

Uso:
    python -m pruebas.anadirTareaPresupuesto_test

Forma parte del entorno de pruebas y desarrollo del sistema ReyBoxes.
"""

import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_anadirTareaPresupuesto import DialogoTarea

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogo = DialogoTarea()

    # Ejecuta el diálogo de tareas y muestra los datos si se acepta correctamente
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

# para ejecutar el modulo desde consola:
# python -m pruebas.pruebas_ventanas.anadirTareaPresupuesto_test
