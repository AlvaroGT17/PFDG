"""
Tests automatizados para la ventana `VentanaNuevoClienteCompraventas`.

Este conjunto de pruebas valida aspectos básicos de la ventana encargada
del registro de nuevos clientes en la sección de compraventas.

Verifica:
- Que la ventana se inicializa correctamente sin errores.
- Que contiene al menos los campos de texto básicos esperados
  (como nombre, DNI, teléfono, etc.).

"""

import pytest
from PySide6.QtWidgets import QLineEdit
from pruebas.nuevoCliente_compraventas_test import iniciar_ventana_nuevo_cliente


def test_ventana_cliente_compraventa_inicializa(qtbot):
    """
    Verifica que la ventana de nuevo cliente se puede instanciar correctamente
    y que su título no está vacío.
    """
    ventana = iniciar_ventana_nuevo_cliente()
    qtbot.addWidget(ventana)

    assert ventana is not None
    assert ventana.windowTitle() != "", "Falta el título de la ventana."


def test_existen_campos_de_entrada(qtbot):
    """
    Verifica que la ventana contiene al menos tres campos de texto (`QLineEdit`),
    lo cual es esperable para introducir datos como nombre, DNI y teléfono.
    """
    ventana = iniciar_ventana_nuevo_cliente()
    qtbot.addWidget(ventana)

    entradas = ventana.findChildren(QLineEdit)
    assert len(
        entradas) >= 3, "Se esperaban al menos 3 campos de entrada (nombre, dni, teléfono)."
