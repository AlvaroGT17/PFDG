"""
Pruebas unitarias para la clase `VentanaCorreoConfirmacion`.

Este conjunto de pruebas cubre:
- La visibilidad inicial de la ventana.
- El comportamiento al seleccionar las opciones de correo por defecto o personalizado.
- La validación de campos vacíos y la respuesta mediante `QMessageBox.warning`.

Las pruebas utilizan `pytest-qt` para simular la interacción del usuario
y `unittest.mock` para interceptar los mensajes de advertencia.

"""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QRadioButton, QPushButton, QMessageBox
from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion


def test_ventana_visible(qtbot):
    """Verifica que la ventana se muestre correctamente al instanciarse."""
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()
    assert ventana.isVisible()


def test_radio_defecto_seleccionado(qtbot):
    """Al seleccionar la opción por defecto, debe guardarse 'DEFECTO' como valor."""
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()
    ventana.radio_defecto.setChecked(True)
    qtbot.mouseClick(ventana.findChild(QPushButton), Qt.LeftButton)
    assert ventana.correo_seleccionado == "DEFECTO"


def test_radio_personalizado_seleccionado(qtbot):
    """Al escribir un correo personalizado, debe guardarse correctamente como valor."""
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.radio_personalizado.setChecked(True)
    ventana.input_personalizado.setText("otro@test.com")
    qtbot.mouseClick(ventana.findChild(QPushButton), Qt.LeftButton)

    assert ventana.correo_seleccionado == "otro@test.com"


def test_radio_personalizado_vacio_muestra_advertencia(qtbot, mocker):
    """Si el campo personalizado está vacío, debe mostrarse una advertencia."""
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.radio_personalizado.setChecked(True)
    ventana.input_personalizado.setText("")

    mock_warning = mocker.patch.object(QMessageBox, "warning")
    qtbot.mouseClick(ventana.findChild(QPushButton), Qt.LeftButton)
    mock_warning.assert_called_once()


def test_no_seleccionado_muestra_advertencia(qtbot, mocker):
    """Si no se selecciona ninguna opción, debe mostrarse una advertencia."""
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.radio_defecto.setChecked(False)
    ventana.radio_personalizado.setChecked(False)

    mock_warning = mocker.patch.object(QMessageBox, "warning")
    qtbot.mouseClick(ventana.findChild(QPushButton), Qt.LeftButton)
    mock_warning.assert_called_once()
