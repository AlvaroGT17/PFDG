"""
Módulo de prueba para lanzar la ventana de inicio (dashboard principal).

Este archivo permite abrir manualmente la ventana principal (`InicioControlador`)
con un usuario ficticio (nombre y rol), útil para testeo visual de la interfaz,
botones y flujos de navegación, sin necesidad de arrancar toda la aplicación.

También puede ser importado desde pruebas unitarias sin mostrar la interfaz,
gracias a su diseño condicional que detecta si está siendo invocado como test.

Uso manual:
    python -m pruebas.inicio_test
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
        InicioControlador: Controlador ya inicializado y listo para usar.
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
