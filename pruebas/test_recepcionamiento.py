"""
Tests automatizados para `VentanaRecepcionamiento`.

Se validan:
- Inicialización correcta.
- Título definido.
- Comportamiento del botón de borrar.
- Limpieza de campos.
- Eventos de teclado para el modo firma.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

import pytest
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QMessageBox
from pruebas.recepcionamiento_test import iniciar_ventana_recepcionamiento
from unittest.mock import patch


def test_recepcionamiento_se_inicializa(qtbot):
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    assert ventana.windowTitle() != "", "La ventana no tiene título definido."


def test_campos_principales_estan_poblados(qtbot):
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    assert ventana.input_nombre.text() != "", "El campo de nombre está vacío"
    assert ventana.input_matricula.currentText() != "", "El campo matrícula está vacío"


def test_titulo_correcto(qtbot):
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    assert "Recepcionamiento" in ventana.windowTitle()


def test_boton_cancelar_existe(qtbot):
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    assert ventana.boton_cancelar.text().lower() == "cancelar"


def test_boton_borrar_dispara_confirmacion(qtbot, mocker):
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    mock_confirm = mocker.patch.object(
        QMessageBox, "exec", return_value=QMessageBox.Yes)
    mock_borrar = mocker.patch.object(ventana, "borrar_todo")

    ventana.confirmar_borrado()

    mock_confirm.assert_called_once()
    mock_borrar.assert_called_once()


def test_borrar_todo_limpia_campos(qtbot):
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    ventana.input_nombre.setText("Cresnik")
    ventana.input_dni.setText("12345678Z")
    ventana.input_observaciones.setPlainText("Prueba")

    ventana.borrar_todo()

    assert ventana.input_nombre.text() == ""
    assert ventana.input_dni.text() == ""
    assert ventana.input_observaciones.toPlainText() == ""


def test_event_filter_oculta_mensaje_firma(qtbot):
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)

    ventana.modo_firma_activo = True
    ventana.mensaje_firma.setVisible(True)

    evento_enter = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
    handled = ventana.eventFilter(ventana, evento_enter)

    assert handled is True
    assert not ventana.mensaje_firma.isVisible()
