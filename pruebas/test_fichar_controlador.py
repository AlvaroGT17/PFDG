"""
Pruebas unitarias para el controlador FicharControlador.

Se valida el comportamiento del método `fichar`, incluyendo:
- Mostrar error si no se selecciona tipo.
- Llamada a registrar_fichaje con datos correctos.
- Mostrar mensaje de confirmación y cerrar ventana.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

import pytest
from unittest.mock import patch
from controladores.fichar_controlador import FicharControlador
from PySide6.QtWidgets import QMessageBox


@pytest.fixture
def usuario_mock():
    """Usuario simulado para las pruebas."""
    return {"id": 123, "nombre": "JUAN", "rol": "Mecánico"}


@pytest.fixture
def controlador(qtbot, usuario_mock):
    """Inicializa el controlador con su ventana y la registra en QtBot."""
    ctrl = FicharControlador(usuario_mock)
    qtbot.addWidget(ctrl.ventana)
    return ctrl


def test_fichar_sin_seleccion_muestra_error(controlador, mocker):
    """
    Si no se selecciona ni 'Entrada' ni 'Salida', debe mostrarse una advertencia.
    """
    mock_warning = mocker.patch.object(QMessageBox, "warning")

    # Simular que no se ha seleccionado ningún tipo
    controlador.ventana.radio_entrada.setChecked(False)
    controlador.ventana.radio_salida.setChecked(False)

    controlador.fichar()

    mock_warning.assert_called_once_with(
        controlador.ventana, "Fichaje inválido", "Debes seleccionar 'Entrada' o 'Salida'"
    )


@patch("controladores.fichar_controlador.registrar_fichaje")
def test_fichar_con_entrada_llama_a_registrar(mock_registrar, controlador, mocker):
    """
    Si se selecciona 'Entrada', debe llamarse a `registrar_fichaje` correctamente
    y mostrarse un mensaje de confirmación.
    """
    mock_info = mocker.patch.object(QMessageBox, "information")
    mock_close = mocker.patch.object(controlador.ventana, "close")

    controlador.ventana.radio_entrada.setChecked(True)

    controlador.fichar()

    mock_registrar.assert_called_once_with(123, "ENTRADA")
    mock_info.assert_called_once_with(
        controlador.ventana, "Fichaje registrado", "Fichaje de ENTRADA registrado correctamente."
    )
    mock_close.assert_called_once()


@patch("controladores.fichar_controlador.registrar_fichaje")
def test_fichar_con_salida_llama_a_registrar(mock_registrar, controlador, mocker):
    """
    Si se selecciona 'Salida', debe llamarse a `registrar_fichaje` correctamente
    y mostrarse un mensaje de confirmación.
    """
    mock_info = mocker.patch.object(QMessageBox, "information")
    mock_close = mocker.patch.object(controlador.ventana, "close")

    controlador.ventana.radio_salida.setChecked(True)

    controlador.fichar()

    mock_registrar.assert_called_once_with(123, "SALIDA")
    mock_info.assert_called_once_with(
        controlador.ventana, "Fichaje registrado", "Fichaje de SALIDA registrado correctamente."
    )
    mock_close.assert_called_once()
