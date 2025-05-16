"""
Pruebas unitarias para el controlador `CrearClienteRapidoControlador`.

Se verifican los siguientes escenarios:
- Validación de DNI incorrecto.
- Detección de DNI duplicado.
- Fallo al intentar insertar un nuevo cliente.
- Éxito en la creación de cliente y emisión de señal.

Las funciones dependientes (`validar_dni`, `dni_ya_existe`, `crear_cliente_y_devolver_id`)
se simulan con mocks para evitar acceso real a base de datos o ventanas de diálogo.

Autor: Cresnik
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

import pytest
from unittest.mock import patch, MagicMock
from controladores.crear_cliente_rapido_controlador import CrearClienteRapidoControlador


@pytest.fixture
def controlador(qtbot):
    """
    Fixture que inicializa el controlador `CrearClienteRapidoControlador`
    y agrega su ventana al entorno de prueba Qt.
    """
    ctrl = CrearClienteRapidoControlador()
    qtbot.addWidget(ctrl.ventana)
    return ctrl


@patch("controladores.crear_cliente_rapido_controlador.QMessageBox.exec")
@patch("controladores.crear_cliente_rapido_controlador.DNIUtils.validar_dni", return_value=False)
def test_dni_invalido_muestra_error(mock_validar, mock_msgbox, controlador):
    """
    Si el DNI es inválido, se debe mostrar un mensaje de error
    y no continuar con la creación del cliente.
    """
    controlador.ventana.input_nombre.setText("TEST")
    controlador.ventana.input_apellido1.setText("APELLIDO")
    controlador.ventana.input_dni.setText("INVALIDO")
    controlador.ventana.input_telefono.setText("600000000")

    controlador.crear_cliente()

    mock_msgbox.assert_called_once()
    assert mock_validar.called


@patch("controladores.crear_cliente_rapido_controlador.QMessageBox.exec")
@patch("controladores.crear_cliente_rapido_controlador.DNIUtils.validar_dni", return_value=True)
@patch("controladores.crear_cliente_rapido_controlador.dni_ya_existe", return_value=True)
def test_dni_duplicado_muestra_error(mock_existe, mock_validar, mock_msgbox, controlador):
    """
    Si el DNI ya existe en la base de datos, debe mostrarse un mensaje de advertencia.
    """
    controlador.ventana.input_nombre.setText("TEST")
    controlador.ventana.input_apellido1.setText("APELLIDO")
    controlador.ventana.input_dni.setText("12345678Z")
    controlador.ventana.input_telefono.setText("600000000")

    controlador.crear_cliente()

    mock_msgbox.assert_called_once()
    assert mock_existe.called


@patch("controladores.crear_cliente_rapido_controlador.QMessageBox.exec")
@patch("controladores.crear_cliente_rapido_controlador.DNIUtils.validar_dni", return_value=True)
@patch("controladores.crear_cliente_rapido_controlador.dni_ya_existe", return_value=False)
@patch("controladores.crear_cliente_rapido_controlador.crear_cliente_y_devolver_id", return_value=None)
def test_error_al_crear_cliente_muestra_error(mock_insert, mock_existe, mock_validar, mock_msgbox, controlador):
    """
    Si ocurre un error al insertar el cliente, se debe mostrar un mensaje de error.
    """
    controlador.ventana.input_nombre.setText("TEST")
    controlador.ventana.input_apellido1.setText("APELLIDO")
    controlador.ventana.input_dni.setText("12345678Z")
    controlador.ventana.input_telefono.setText("600000000")

    controlador.crear_cliente()

    mock_msgbox.assert_called_once()
    assert mock_insert.called


@patch("controladores.crear_cliente_rapido_controlador.QMessageBox.exec")
@patch("controladores.crear_cliente_rapido_controlador.DNIUtils.validar_dni", return_value=True)
@patch("controladores.crear_cliente_rapido_controlador.dni_ya_existe", return_value=False)
@patch("controladores.crear_cliente_rapido_controlador.crear_cliente_y_devolver_id", return_value=42)
def test_cliente_creado_correctamente(mock_insert, mock_existe, mock_validar, mock_msgbox, controlador, qtbot):
    """
    Si el cliente se crea correctamente, debe emitirse la señal con los datos
    y mostrarse un mensaje de éxito.
    """
    resultado = {}

    def receptor(cliente_dict):
        resultado.update(cliente_dict)

    controlador.cliente_creado.connect(receptor)

    controlador.ventana.input_nombre.setText("JUAN")
    controlador.ventana.input_apellido1.setText("LOPEZ")
    controlador.ventana.input_dni.setText("12345678Z")
    controlador.ventana.input_telefono.setText("600000000")

    controlador.crear_cliente()

    assert resultado["id"] == 42
    assert resultado["nombre"] == "JUAN"
    assert resultado["primer_apellido"] == "LOPEZ"
    assert resultado["dni"] == "12345678Z"
    mock_msgbox.assert_called_once()
