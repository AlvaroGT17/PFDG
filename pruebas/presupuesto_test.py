"""
Script de prueba para lanzar manualmente la ventana de presupuestos.

Se utiliza tanto para testeo visual como para importar desde tests automatizados.
"""

import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_presupuesto import VentanaPresupuesto
from controladores.presupuesto_controlador import PresupuestoControlador


def iniciar_ventana_presupuesto():
    """
    Inicializa la ventana de presupuestos sin mostrarla (para pruebas unitarias).
    """
    ventana = VentanaPresupuesto()
    PresupuestoControlador(ventana)
    return ventana


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = iniciar_ventana_presupuesto()
    ventana.exec()  # Modal (bloquea hasta que se cierre)

    sys.exit()
