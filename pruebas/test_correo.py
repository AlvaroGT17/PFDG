import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QRadioButton, QPushButton, QMessageBox
from vistas.ventana_correo_confirmacion import VentanaCorreoConfirmacion


def test_ventana_visible(qtbot):
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()
    assert ventana.isVisible()


def test_radio_defecto_seleccionado(qtbot):
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()
    ventana.radio_defecto.setChecked(True)
    qtbot.mouseClick(ventana.findChild(QPushButton), Qt.LeftButton)
    assert ventana.correo_seleccionado == "DEFECTO"


def test_radio_personalizado_seleccionado(qtbot):
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.radio_personalizado.setChecked(True)
    ventana.input_personalizado.setText("otro@test.com")
    qtbot.mouseClick(ventana.findChild(QPushButton), Qt.LeftButton)

    assert ventana.correo_seleccionado == "otro@test.com"


def test_radio_personalizado_vacio_muestra_advertencia(qtbot, mocker):
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.radio_personalizado.setChecked(True)
    ventana.input_personalizado.setText("")

    mock_warning = mocker.patch.object(QMessageBox, "warning")
    qtbot.mouseClick(ventana.findChild(QPushButton), Qt.LeftButton)
    mock_warning.assert_called_once()


def test_no_seleccionado_muestra_advertencia(qtbot, mocker):
    ventana = VentanaCorreoConfirmacion("cliente@test.com")
    qtbot.addWidget(ventana)
    ventana.show()

    ventana.radio_defecto.setChecked(False)
    ventana.radio_personalizado.setChecked(False)

    mock_warning = mocker.patch.object(QMessageBox, "warning")
    qtbot.mouseClick(ventana.findChild(QPushButton), Qt.LeftButton)
    mock_warning.assert_called_once()
