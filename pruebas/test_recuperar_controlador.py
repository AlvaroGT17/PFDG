"""
TEST UNITARIO: Controlador de recuperación de cuenta (RecuperarControlador)

Este módulo realiza pruebas sobre la lógica de la clase RecuperarControlador,
encargada de gestionar la recuperación de cuenta mediante código OTP enviado
al correo electrónico.

Objetivos:
- Validar la conexión de señales (ej. botón volver).
- Comprobar la lógica de validación del correo.
- Asegurar el comportamiento esperado al enviar código de recuperación.
- Verificar los mensajes mostrados al usuario en distintos escenarios.

Requiere:
- pytest
- PySide6
"""

import pytest
from unittest.mock import patch, MagicMock
from controladores.recuperar_controlador import RecuperarControlador


@pytest.fixture
def controlador():
    """
    Crea una instancia del controlador con ventana simulada para pruebas.

    Returns:
        RecuperarControlador: Controlador con componentes simulados.
    """
    with patch("controladores.recuperar_controlador.VentanaRecuperar") as MockVentana:
        ventana_mock = MockVentana.return_value
        ventana_mock.input_correo.text.return_value = ""
        ventana_mock.btn_enviar = MagicMock()
        ventana_mock.btn_volver = MagicMock()
        return RecuperarControlador()


def test_se_conecta_senal_volver(controlador):
    """
    Verifica que la señal del botón 'Volver' esté conectada.
    """
    assert controlador.ventana.btn_volver.clicked.connect.called


def test_validar_correo_activa_boton_si_valido(controlador):
    """
    Si el correo es válido, el botón de enviar debe habilitarse.
    """
    controlador.ventana.input_correo.text.return_value = "correo@valido.com"
    controlador.validar_correo()
    controlador.ventana.btn_enviar.setEnabled.assert_called_with(True)


def test_validar_correo_desactiva_boton_si_invalido(controlador):
    """
    Si el correo es inválido, el botón de enviar debe deshabilitarse.
    """
    controlador.ventana.input_correo.text.return_value = "correo_invalido"
    controlador.validar_correo()
    controlador.ventana.btn_enviar.setEnabled.assert_called_with(False)


def test_enviar_codigo_muestra_warning_si_vacio(controlador):
    """
    Si el campo de correo está vacío, debe mostrarse un mensaje de advertencia.
    """
    controlador.ventana.input_correo.text.return_value = ""
    with patch("controladores.recuperar_controlador.QMessageBox.warning") as mock_warning:
        controlador.enviar_codigo()
        assert mock_warning.called


def test_enviar_codigo_muestra_warning_si_no_usuario(controlador):
    """
    Si el correo no está asociado a ningún usuario, debe mostrarse advertencia.
    """
    controlador.ventana.input_correo.text.return_value = "noexiste@correo.com"
    with patch("controladores.recuperar_controlador.obtener_usuario_por_email", return_value=None), \
            patch("controladores.recuperar_controlador.QMessageBox.warning") as mock_warning:
        controlador.enviar_codigo()
        assert mock_warning.called


def test_enviar_codigo_ok():
    """
    Si todo va bien (usuario existe, se guarda y se envía el código),
    el envío de correo debe ejecutarse correctamente.
    """
    with patch("controladores.recuperar_controlador.VentanaRecuperar") as MockVentana, \
            patch("controladores.recuperar_controlador.obtener_usuario_por_email", return_value={"id": 1, "nombre": "Cresnik"}), \
            patch("controladores.recuperar_controlador.guardar_codigo_recuperacion", return_value=True), \
            patch("controladores.recuperar_controlador.enviar_correo") as mock_enviar, \
            patch("controladores.recuperar_controlador.VerificarControlador") as mock_verificar:

        ventana_mock = MockVentana.return_value
        ventana_mock.input_correo.text.return_value = "test@correo.com"
        ventana_mock.btn_enviar = MagicMock()
        ventana_mock.btn_volver = MagicMock()

        controlador = RecuperarControlador()
        controlador.enviar_codigo()
        assert mock_enviar.called


def test_enviar_codigo_falla_guardado():
    """
    Si guardar el código de recuperación falla, debe mostrarse advertencia.
    """
    with patch("controladores.recuperar_controlador.VentanaRecuperar") as MockVentana, \
            patch("controladores.recuperar_controlador.obtener_usuario_por_email", return_value={"id": 1, "nombre": "Cresnik"}), \
            patch("controladores.recuperar_controlador.guardar_codigo_recuperacion", return_value=False), \
            patch("controladores.recuperar_controlador.QMessageBox.warning") as mock_warning:

        ventana_mock = MockVentana.return_value
        ventana_mock.input_correo.text.return_value = "test@correo.com"
        ventana_mock.btn_enviar = MagicMock()
        ventana_mock.btn_volver = MagicMock()

        controlador = RecuperarControlador()
        controlador.enviar_codigo()
        assert mock_warning.called


def test_enviar_codigo_falla_envio():
    """
    Si el envío del correo falla, debe mostrarse un mensaje de error crítico.
    """
    with patch("controladores.recuperar_controlador.VentanaRecuperar") as MockVentana, \
            patch("controladores.recuperar_controlador.obtener_usuario_por_email", return_value={"id": 1, "nombre": "Cresnik"}), \
            patch("controladores.recuperar_controlador.guardar_codigo_recuperacion", return_value=True), \
            patch("controladores.recuperar_controlador.enviar_correo", side_effect=Exception("Fallo")), \
            patch("controladores.recuperar_controlador.QMessageBox.critical") as mock_critical:

        ventana_mock = MockVentana.return_value
        ventana_mock.input_correo.text.return_value = "test@correo.com"
        ventana_mock.btn_enviar = MagicMock()
        ventana_mock.btn_volver = MagicMock()

        controlador = RecuperarControlador()
        controlador.enviar_codigo()
        assert mock_critical.called


def test_volver_emite_senal(qtbot):
    """
    La función volver debe emitir la señal senal_volver_login correctamente.
    """
    controlador = RecuperarControlador()
    with qtbot.waitSignal(controlador.senal_volver_login, timeout=1000):
        controlador.volver()
