# pruebas/test_login_controlador.py
import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QMessageBox
from controladores.login_controlador import LoginControlador

# 💡 Fixture global para evitar que QMessageBox muestre ventanas reales


@pytest.fixture(autouse=True)
def desactivar_qmessagebox():
    QMessageBox.information = MagicMock()
    QMessageBox.warning = MagicMock()
    QMessageBox.critical = MagicMock()


@pytest.fixture
def controlador(qtbot):
    c = LoginControlador()
    qtbot.addWidget(c.ventana)
    return c


def test_abrir_recuperacion_emite_senal(controlador, qtbot):
    with patch.object(controlador, "cerrar") as mock_cerrar:
        llamada = []

        def capturar():
            llamada.append(True)

        controlador.senal_abrir_recuperacion.connect(capturar)
        controlador.abrir_recuperacion()

        assert llamada, "No se emitió la señal de recuperación"
        mock_cerrar.assert_called_once()


def test_login_campos_vacios_muestra_warning(controlador):
    controlador.ventana.input_usuario.setText("")
    controlador.ventana.input_contrasena.setText("")

    controlador.iniciar_proceso_login()

    QMessageBox.warning.assert_called_once()
    args = QMessageBox.warning.call_args[0]
    assert "Falta el nombre" in args[2]
    assert "Falta la contraseña" in args[2]


@patch("controladores.login_controlador.obtener_usuario_por_nombre")
@patch("controladores.login_controlador.verificar_contrasena")
def test_login_correcto_emite_senal(mock_verificar, mock_obtener, controlador):
    usuario_ficticio = {"nombre": "CRESNIK", "password": "hash", "id": 1}
    mock_obtener.return_value = usuario_ficticio
    mock_verificar.return_value = True

    controlador.ventana.input_usuario.setText("CRESNIK")
    controlador.ventana.input_contrasena.setText("1234")
    controlador.ventana_carga = MagicMock()

    llamada = []
    controlador.senal_login_exitoso.connect(lambda user: llamada.append(user))

    with patch.object(controlador, "cerrar"):
        controlador.validar_login("CRESNIK", "1234")

    controlador.ventana_carga.cerrar.assert_called_once()
    QMessageBox.information.assert_called_once()
    assert llamada and llamada[0]["nombre"] == "CRESNIK"


@patch("controladores.login_controlador.obtener_usuario_por_nombre")
@patch("controladores.login_controlador.verificar_contrasena")
def test_login_fallido_muestra_error(mock_verificar, mock_obtener, controlador):
    mock_obtener.return_value = None
    mock_verificar.return_value = False

    controlador.ventana_carga = MagicMock()
    controlador.validar_login("MALO", "1234")

    controlador.ventana_carga.cerrar.assert_called_once()
    QMessageBox.critical.assert_called_once()
    assert "incorrectos" in QMessageBox.critical.call_args[0][2]
