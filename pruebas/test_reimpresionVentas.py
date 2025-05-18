"""
TESTS AUTOMÁTICOS: Ventana de Reimpresión de Ventas (`VentanaReimpresionVentas`)

Este módulo valida el correcto funcionamiento visual y estructural
de la interfaz gráfica encargada de mostrar documentos PDF de ventas
para su reimpresión, envío o visualización.

Pruebas incluidas:
- Comprobación de componentes visibles y etiquetados.
- Validación de configuración de la tabla de documentos.
- Gestión de errores al intentar abrir un archivo inexistente.

Requiere:
- pytest
- pytest-qt
- PySide6
"""

import os
import pytest
from PySide6.QtWidgets import (
    QPushButton, QTableWidgetItem, QTableWidget,
    QMessageBox, QAbstractItemView
)
from vistas.ventana_reimpresionVentas import VentanaReimpresionVentas
from unittest.mock import patch


def iniciar_ventana_reimpresion_ventas():
    """
    Inicializa una instancia de la ventana de reimpresión de ventas.

    Returns:
        VentanaReimpresionVentas: Ventana lista para testeo.
    """
    return VentanaReimpresionVentas("Usuario", "admin", lambda: None)


def test_reimpresion_ventas_componentes(qtbot):
    """
    TEST 1: Componentes esenciales visibles

    Verifica que:
    - La tabla principal tiene 3 columnas.
    - Existen botones con texto "Volver", "Enviar" e "Imprimir".
    """
    ventana = iniciar_ventana_reimpresion_ventas()
    qtbot.addWidget(ventana)
    ventana.show()

    tabla = ventana.findChild(QTableWidget)
    assert tabla is not None
    assert tabla.columnCount() == 3

    botones = ventana.findChildren(QPushButton)
    textos = [btn.text().lower() for btn in botones]

    assert any("volver" in t for t in textos), "Botón 'Volver' no encontrado"
    assert any("enviar" in t for t in textos), "Botón 'Enviar' no encontrado"
    assert any("imprimir" in t for t in textos), "Botón 'Imprimir' no encontrado"


def test_tabla_configurada_correctamente(qtbot):
    """
    TEST 2: Configuración de tabla

    Valida que:
    - La tabla selecciona filas completas.
    - No permite edición directa.
    - Aplica colores alternos por fila.
    - Oculta la columna de ruta (índice 2).
    """
    ventana = iniciar_ventana_reimpresion_ventas()
    qtbot.addWidget(ventana)
    tabla = ventana.tabla

    assert tabla.selectionBehavior() == QAbstractItemView.SelectRows
    assert not tabla.editTriggers() & QAbstractItemView.AllEditTriggers
    assert tabla.alternatingRowColors()
    assert tabla.isColumnHidden(2)


def test_abrir_documento_no_existente_muestra_warning(qtbot, mocker):
    """
    TEST 3: Intento de abrir documento inexistente

    Simula el doble clic sobre una fila cuya ruta apunta a un archivo inexistente.
    Verifica que se lanza un QMessageBox de advertencia.
    """
    ventana = iniciar_ventana_reimpresion_ventas()
    qtbot.addWidget(ventana)

    ventana.tabla.setRowCount(1)
    ventana.tabla.setItem(0, 2, QTableWidgetItem("ruta/inexistente.pdf"))

    mock_warning = mocker.patch("PySide6.QtWidgets.QMessageBox.warning")
    ventana.abrir_documento_seleccionado(0, 0)
    mock_warning.assert_called_once()
