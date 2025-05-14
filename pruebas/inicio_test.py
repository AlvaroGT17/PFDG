"""
Módulo de prueba para lanzar la ventana de inicio (dashboard principal).

Puede ejecutarse manualmente o ser importado en tests automatizados
sin mostrar la ventana.
"""

import sys
from controladores.inicio_controlador import InicioControlador

# Indicador de si se está ejecutando como test
setattr(sys, "_called_from_test", False)


def iniciar_ventana_inicio():
    """
    Crea una instancia del controlador de la ventana de inicio (dashboard)
    con un usuario ficticio.

    Returns:
        InicioControlador: Controlador ya inicializado.
    """
    nombre = "CRESNIK"
    rol = "Administrador"
    return InicioControlador(nombre, rol)


# Solo ejecuta visualmente si es lanzado manualmente y no desde pytest
if __name__ == "__main__" and not getattr(sys, "_called_from_test", False):
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    controlador = iniciar_ventana_inicio()
    controlador.senal_cerrar_sesion.connect(app.quit)
    controlador.mostrar()

    sys.exit(app.exec())
