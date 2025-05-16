"""
TEST: Ventana de historial de fichajes

Verifica que la ventana `VentanaHistorial` puede crearse correctamente con PySide6
y que la tabla tiene al menos una columna.
"""

import pytest
from PySide6.QtWidgets import QTableWidget
from controladores.historial_controlador import HistorialControlador
from datetime import datetime
from PySide6.QtWidgets import QTableWidget, QToolButton
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


def test_botones_existen_y_tienen_iconos(qtbot):
    """
    Verifica que los botones CSV, PDF y Volver existen, tienen texto e icono.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=False)
    qtbot.addWidget(controlador.ventana)

    ventana = controlador.ventana

    for boton in [ventana.boton_csv, ventana.boton_pdf, ventana.boton_volver]:
        assert isinstance(boton, QToolButton)
        assert boton.icon().isNull() is False
        assert boton.text() != ""


def test_cargar_datos_tabla(qtbot):
    """
    Verifica que la tabla carga correctamente los datos proporcionados.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=False)
    qtbot.addWidget(controlador.ventana)

    datos = [
        (datetime(2025, 5, 15, 9, 0), "ENTRADA", "JUAN PÉREZ"),
        (datetime(2025, 5, 15, 17, 30), "SALIDA", "JUAN PÉREZ"),
    ]

    controlador.ventana.cargar_datos(datos)
    tabla = controlador.ventana.tabla

    assert tabla.rowCount() == 2
    assert tabla.item(0, 0).text() == "2025-05-15 09:00:00"
    assert tabla.item(1, 1).text() == "SALIDA"
    assert tabla.item(1, 2).text() == "JUAN PÉREZ"


def test_colores_aplicados_por_tipo(qtbot):
    """
    Verifica que los colores de fondo en la tabla se aplican según el tipo de fichaje.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=False)
    qtbot.addWidget(controlador.ventana)

    datos = [
        (datetime.now(), "ENTRADA", "Usuario A"),
        (datetime.now(), "SALIDA", "Usuario B"),
    ]
    controlador.ventana.cargar_datos(datos)

    entrada_color = controlador.ventana.tabla.item(
        0, 0).background().color().name()
    salida_color = controlador.ventana.tabla.item(
        1, 0).background().color().name()

    assert entrada_color.lower() == "#fff8cc"
    assert salida_color.lower() == "#e0f0ff"
