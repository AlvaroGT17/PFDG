"""
Tests para la ventana `VentanaHistorial` del sistema de fichajes.

Este conjunto de pruebas valida los siguientes aspectos:
- Que la ventana se inicializa correctamente.
- Que la tabla de fichajes está presente y contiene columnas.
- Que los botones de acción (CSV, PDF, Volver) existen y están correctamente configurados.
- Que los datos de fichajes se cargan correctamente en la tabla.
- Que los colores aplicados a las filas de la tabla se ajustan según el tipo de fichaje.

"""

import pytest
from PySide6.QtWidgets import QTableWidget, QToolButton
from controladores.historial_controlador import HistorialControlador
from datetime import datetime


def test_historial_crea_ventana_correctamente(qtbot):
    """
    Verifica que la instancia del controlador de historial se crea correctamente 
    y que la ventana tiene un título válido.
    """
    usuario_id = 1
    es_admin = False

    controlador = HistorialControlador(usuario_id, es_admin)
    qtbot.addWidget(controlador.ventana)

    assert controlador.ventana is not None
    assert controlador.ventana.windowTitle() != ""


def test_historial_contiene_tabla(qtbot):
    """
    Verifica que la ventana contiene una tabla (`QTableWidget`) con al menos una columna.
    """
    controlador = HistorialControlador(usuario_id=1, es_admin=False)
    qtbot.addWidget(controlador.ventana)

    tabla = controlador.ventana.findChild(QTableWidget)
    assert tabla is not None, "No se encontró la tabla en la ventana."
    assert tabla.columnCount() > 0, "La tabla no tiene columnas definidas."


def test_botones_existen_y_tienen_iconos(qtbot):
    """
    Comprueba que los botones de exportación (CSV, PDF) y el botón Volver:
    - Existen en la ventana.
    - Son instancias de `QToolButton`.
    - Tienen texto asignado.
    - Tienen un icono visible.
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
    Verifica que el método `cargar_datos()` llena correctamente la tabla
    con los registros de fichajes proporcionados.
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
    Verifica que los colores de fondo de las filas de la tabla se aplican correctamente 
    según el tipo de fichaje (ENTRADA o SALIDA), usando los colores definidos en la lógica.
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

    assert entrada_color.lower() == "#fff8cc"  # Color definido para ENTRADA
    assert salida_color.lower() == "#e0f0ff"  # Color definido para SALIDA
