"""
Script de prueba para abrir manualmente la ventana `VentanaNuevoClienteCompraventas`.

Este módulo permite lanzar la ventana de forma visual sin necesidad de ejecutar 
toda la aplicación. También puede importarse desde pruebas unitarias para verificar
comportamiento, validaciones o disposición visual de los campos.

Uso:
    python -m pruebas.nuevoCliente_compraventas_test
"""

import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_nuevoCliente_compraventas import VentanaNuevoClienteCompraventas


def guardar_cliente_simulado(datos):
    """
    Simula el guardado de datos del cliente, imprimiéndolos en consola.

    Args:
        datos (dict): Datos del cliente que serían guardados.
    """
    print("📝 Cliente capturado desde test:", datos)


def iniciar_ventana_nuevo_cliente():
    """
    Devuelve una instancia de la ventana de nuevo cliente, con un callback simulado.

    Returns:
        VentanaNuevoClienteCompraventas: Instancia lista para ser mostrada o usada en tests.
    """
    return VentanaNuevoClienteCompraventas(callback_guardar=guardar_cliente_simulado)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = iniciar_ventana_nuevo_cliente()
    ventana.show()
    sys.exit(app.exec())
