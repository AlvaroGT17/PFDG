"""
Tests automatizados para la ventana de presupuestos.

Comprueba:
- Que la ventana se instancia correctamente.
- Que el título está definido.
- Que hay elementos básicos como `QLineEdit`, `QComboBox`, etc.
"""

import pytest
from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit
from pruebas.presupuesto_test import iniciar_ventana_presupuesto


def test_ventana_presupuesto_inicializa(qtbot):
    """
    Verifica que la ventana de presupuesto se carga sin errores.
    """
    ventana = iniciar_ventana_presupuesto()
    qtbot.addWidget(ventana)

    assert ventana is not None
    assert ventana.windowTitle() != "", "La ventana no tiene título."


def test_hay_campos_principales(qtbot):
    """
    Verifica que la ventana tiene campos clave como campos de texto y área de comentarios.
    """
    ventana = iniciar_ventana_presupuesto()
    qtbot.addWidget(ventana)

    entradas = ventana.findChildren(QLineEdit)
    textos = ventana.findChildren(QTextEdit)

    assert len(entradas) >= 3, "Faltan campos QLineEdit"
    assert len(textos) >= 1, "Falta el campo de comentarios (QTextEdit)"
