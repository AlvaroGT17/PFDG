"""
Script de prueba para abrir manualmente la ventana `VentanaNuevoClienteCompraventas`.

Permite probar la interfaz de forma visual o integrarla en pruebas unitarias.
"""

import sys
from PySide6.QtWidgets import QApplication
from vistas.ventana_nuevoCliente_compraventas import VentanaNuevoClienteCompraventas


def guardar_cliente_simulado(datos):
    """
    Simula el guardado de datos. Solo imprime la salida para pruebas.
    """
    print("📝 Cliente capturado desde test:", datos)


def iniciar_ventana_nuevo_cliente():
    """
    Devuelve una instancia de la ventana sin mostrarla (para pruebas automáticas).
    """
    return VentanaNuevoClienteCompraventas(callback_guardar=guardar_cliente_simulado)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = iniciar_ventana_nuevo_cliente()
    ventana.show()
    sys.exit(app.exec())
