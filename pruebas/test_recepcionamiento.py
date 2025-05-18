"""
TEST UNITARIO: Ventana de Recepcionamiento

Este módulo contiene pruebas automatizadas para la clase `VentanaRecepcionamiento`.

Se validan los siguientes aspectos:
- Inicialización correcta de la interfaz.
- Presencia de campos esenciales con valores predeterminados.
- Título de la ventana.
- Existencia y funcionalidad del botón "Cancelar".
- Comportamiento del método `confirmar_borrado`.
- Funcionamiento de `borrar_todo`.
- Gestión del evento Enter en modo firma.

Requiere:
- pytest
- pytest-qt
- PySide6
"""

import pytest
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QMessageBox
from pruebas.recepcionamiento_test import iniciar_ventana_recepcionamiento
from unittest.mock import patch


def test_recepcionamiento_se_inicializa(qtbot):
    """
    Verifica que la ventana se inicializa correctamente con título definido.
    """
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    assert ventana.windowTitle() != "", "La ventana no tiene título definido."


def test_campos_principales_estan_poblados(qtbot):
    """
    Comprueba que los campos esenciales se encuentran poblados por defecto.
    """
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    assert ventana.input_nombre.text() != "", "El campo de nombre está vacío"
    assert ventana.input_matricula.currentText() != "", "El campo matrícula está vacío"


def test_titulo_correcto(qtbot):
    """
    Verifica que el título de la ventana contiene la palabra 'Recepcionamiento'.
    """
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    assert "Recepcionamiento" in ventana.windowTitle()


def test_boton_cancelar_existe(qtbot):
    """
    Verifica que el botón de cancelar está presente y correctamente etiquetado.
    """
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)
    assert ventana.boton_cancelar.text().lower() == "cancelar"


def test_boton_borrar_dispara_confirmacion(qtbot, mocker):
    """
    Verifica que al pulsar el botón borrar se lanza un mensaje de confirmación,
    y si se acepta, se ejecuta la función de borrado.
    """
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)

    mock_confirm = mocker.patch.object(
        QMessageBox, "exec", return_value=QMessageBox.Yes)
    mock_borrar = mocker.patch.object(ventana, "borrar_todo")

    ventana.confirmar_borrado()

    mock_confirm.assert_called_once()
    mock_borrar.assert_called_once()


def test_borrar_todo_limpia_campos(qtbot):
    """
    Verifica que al ejecutar `borrar_todo()` se limpian correctamente
    los campos de texto del formulario.
    """
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
    """
    Verifica que al presionar Enter en modo firma activo,
    se oculta correctamente el mensaje de ayuda.
    """
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)

    ventana.modo_firma_activo = True
    ventana.mensaje_firma.setVisible(True)

    evento_enter = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
    handled = ventana.eventFilter(ventana, evento_enter)

    assert handled is True
    assert not ventana.mensaje_firma.isVisible()
