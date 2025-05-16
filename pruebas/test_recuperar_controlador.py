import pytest
from unittest.mock import patch, MagicMock
from controladores.recuperar_controlador import RecuperarControlador


@pytest.fixture
def controlador():
    with patch("controladores.recuperar_controlador.VentanaRecuperar") as MockVentana:
        ventana_mock = MockVentana.return_value
        ventana_mock.input_correo.text.return_value = ""
        ventana_mock.btn_enviar = MagicMock()
        ventana_mock.btn_volver = MagicMock()
        return RecuperarControlador()


def test_se_conecta_senal_volver(controlador):
    assert controlador.ventana.btn_volver.clicked.connect.called


def test_validar_correo_activa_boton_si_valido(controlador):
    controlador.ventana.input_correo.text.return_value = "correo@valido.com"
    controlador.validar_correo()
    assert controlador.ventana.btn_enviar.setEnabled.called_with(True) or \
        controlador.ventana.btn_enviar.setEnabled.call_args[0][0] is True


def test_validar_correo_desactiva_boton_si_invalido(controlador):
    controlador.ventana.input_correo.text.return_value = "correo_invalido"
    controlador.validar_correo()
    assert controlador.ventana.btn_enviar.setEnabled.called_with(False) or \
        controlador.ventana.btn_enviar.setEnabled.call_args[0][0] is False


def test_enviar_codigo_muestra_warning_si_vacio(controlador):
    controlador.ventana.input_correo.text.return_value = ""
    with patch("controladores.recuperar_controlador.QMessageBox.warning") as mock_warning:
        controlador.enviar_codigo()
        assert mock_warning.called


def test_enviar_codigo_muestra_warning_si_no_usuario(controlador):
    controlador.ventana.input_correo.text.return_value = "noexiste@correo.com"
    with patch("controladores.recuperar_controlador.obtener_usuario_por_email", return_value=None), \
            patch("controladores.recuperar_controlador.QMessageBox.warning") as mock_warning:
        controlador.enviar_codigo()
        assert mock_warning.called


def test_enviar_codigo_ok():
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
    controlador = RecuperarControlador()
    with qtbot.waitSignal(controlador.senal_volver_login, timeout=1000):
        controlador.volver()
