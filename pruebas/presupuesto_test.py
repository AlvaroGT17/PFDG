"""
Script de prueba para lanzar manualmente la ventana de presupuestos.

Este módulo permite abrir la ventana `VentanaPresupuesto` de forma aislada,
ya sea para realizar pruebas visuales durante el desarrollo o para inicializarla
desde tests automatizados.

Puede ejecutarse directamente desde la terminal para comprobar estilos, comportamiento
modal, o integraciones con su controlador asociado (`PresupuestoControlador`).
"""

import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_presupuesto import VentanaPresupuesto
from controladores.presupuesto_controlador import PresupuestoControlador


def iniciar_ventana_presupuesto():
    """
    Inicializa la ventana de presupuestos sin mostrarla (para pruebas unitarias).

    Returns:
        VentanaPresupuesto: Instancia preparada con su controlador asignado.
    """
    ventana = VentanaPresupuesto()
    PresupuestoControlador(ventana)
    return ventana


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = iniciar_ventana_presupuesto()
    ventana.exec()  # Modal (bloquea hasta que se cierre)

    sys.exit()
