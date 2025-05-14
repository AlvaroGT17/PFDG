"""
Módulo de pruebas para la ventana de compraventa.

Se testean tanto operaciones de carga de datos de cliente y vehículo,
como los flujos de contratación de compra y venta, incluyendo:
- Comprobación de valores visuales
- Simulaciones de firma
- Generación de contratos

Autor: Cresnik
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QApplication

from pruebas.compraventa_test import iniciar_ventana_compraventa


@pytest.fixture
def ventana(qtbot):
    vista = iniciar_ventana_compraventa()
    qtbot.addWidget(vista)
    vista.show()
    qtbot.waitExposed(vista)
    qtbot.wait(300)
    return vista


def test_ventana_compraventa_carga_correcta(ventana):
    assert ventana.cliente_nombre.text() == "SERGIO CABRERA PEÑA"
    assert ventana.vehiculo_marca.text() == "SEAT"
    assert ventana.vehiculo_precio_compra.text() == "8500"


def test_toggle_firma_compra(qtbot, ventana):
    boton = ventana.boton_activar_firma

    assert not ventana.firma_activa_compra
    assert not ventana.mensaje_firma_compra.isVisible()

    qtbot.mouseClick(boton, Qt.LeftButton)
    qtbot.wait(200)
    QApplication.processEvents()

    assert ventana.firma_activa_compra
    assert ventana.mensaje_firma_compra.isVisible()


def test_toggle_firma_venta(qtbot, ventana):
    boton = ventana.boton_activar_firma_venta

    assert not ventana.firma_activa_venta
    assert not ventana.mensaje_firma_venta.isVisible()

    qtbot.mouseClick(boton, Qt.LeftButton)
    qtbot.wait(200)
    QApplication.processEvents()

    assert ventana.firma_activa_venta
    assert ventana.mensaje_firma_venta.isVisible()


def test_borrar_todo_deja_formulario_limpio(ventana):
    ventana.cliente_nombre.setText("Prueba")
    ventana.vehiculo_marca.setText("Mazda")
    ventana.input_ruta_guardado_compra.setText("/ruta/test")
    ventana.checkbox_imprimir_compra.setChecked(True)
    ventana.checkbox_correo_venta.setChecked(True)
    ventana.combo_operacion.setCurrentIndex(1)

    ventana.borrar_todo()

    assert ventana.cliente_nombre.text() == ""
    assert ventana.vehiculo_marca.text() == ""
    assert ventana.input_ruta_guardado_compra.text() == ""
    assert not ventana.checkbox_imprimir_compra.isChecked()
    assert not ventana.checkbox_correo_venta.isChecked()
    assert ventana.combo_operacion.currentIndex() == 0
    assert not ventana.mensaje_firma_compra.isVisible()
    assert not ventana.mensaje_firma_venta.isVisible()
    assert ventana.boton_activar_firma.text() == "Activar\nfirma"
    assert ventana.boton_activar_firma_venta.text() == "Activar\nfirma"


@patch("PySide6.QtWidgets.QFileDialog.getExistingDirectory", return_value="/ruta/test")
def test_toggle_ruta_guardado_cambia_estado(mock_dialog, qtbot, ventana):
    # Desactivar ruta predeterminada para habilitar input
    ventana.checkbox_ruta_predeterminada_compra.setChecked(True)
    qtbot.wait(100)
    ventana.checkbox_ruta_predeterminada_compra.setChecked(False)
    qtbot.wait(200)
    QApplication.processEvents()

    assert ventana.input_ruta_guardado_compra.isEnabled()
    assert ventana.boton_buscar_ruta_compra.isEnabled()

    # Simular selección manual de carpeta
    ventana.controlador.seleccionar_ruta_guardado_compra()
    qtbot.wait(100)
    QApplication.processEvents()

    assert ventana.input_ruta_guardado_compra.text() == "/ruta/test"


@patch("PySide6.QtWidgets.QMessageBox.warning")
def test_simular_contrato_venta_sin_vehiculo(mock_msg, qtbot, ventana):
    ventana.vehiculos_filtrados = []
    ventana.tabla_vehiculos.setRowCount(0)
    ventana.tabla_vehiculos.clearSelection()

    ventana.controlador.simular_contrato("venta")

    qtbot.wait(200)
    QApplication.processEvents()

    mock_msg.assert_called_once()
