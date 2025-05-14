"""
TEST: Ventana de historial de fichajes

Verifica que la ventana `VentanaHistorial` puede crearse correctamente con PySide6
y que la tabla tiene al menos una columna.
"""

import pytest
from PySide6.QtWidgets import QTableWidget
from controladores.historial_controlador import HistorialControlador


def test_historial_crea_ventana_correctamente(qtbot):
    """
    Crea el controlador de historial con datos simulados y verifica que la ventana se instancia correctamente.
    """
    usuario_id = 1
    es_admin = False

    controlador = HistorialControlador(usuario_id, es_admin)
    qtbot.addWidget(controlador.ventana)

    assert controlador.ventana is not None
    assert controlador.ventana.windowTitle() != ""


def test_historial_contiene_tabla(qtbot):
    """
    Verifica que la ventana contiene una tabla QTableWidget con columnas.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=False)
    qtbot.addWidget(controlador.ventana)

    tabla = controlador.ventana.findChild(QTableWidget)
    assert tabla is not None, "No se encontró la tabla en la ventana."
    assert tabla.columnCount() > 0, "La tabla no tiene columnas definidas."
