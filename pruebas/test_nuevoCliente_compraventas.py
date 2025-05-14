"""
Tests automatizados para la ventana `VentanaNuevoClienteCompraventas`.

Verifica:
- Que se inicializa correctamente.
- Que contiene al menos campos de texto para introducir datos.
"""

import pytest
from PySide6.QtWidgets import QLineEdit
from pruebas.nuevoCliente_compraventas_test import iniciar_ventana_nuevo_cliente


def test_ventana_cliente_compraventa_inicializa(qtbot):
    """
    Verifica que la ventana se instancia sin errores.
    """
    ventana = iniciar_ventana_nuevo_cliente()
    qtbot.addWidget(ventana)

    assert ventana is not None
    assert ventana.windowTitle() != "", "Falta el título de la ventana."


def test_existen_campos_de_entrada(qtbot):
    """
    Verifica que hay al menos 3 campos de texto (nombre, teléfono, etc.).
    """
    ventana = iniciar_ventana_nuevo_cliente()
    qtbot.addWidget(ventana)

    entradas = ventana.findChildren(QLineEdit)
    assert len(
        entradas) >= 3, "Se esperaban al menos 3 campos de entrada (nombre, dni, teléfono)."
