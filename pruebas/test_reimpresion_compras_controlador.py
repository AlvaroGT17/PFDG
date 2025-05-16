import pytest
from unittest.mock import patch, MagicMock
from controladores.reimpresionCompras_controlador import ReimpresionComprasControlador
from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
from PySide6.QtWidgets import QMessageBox


@pytest.fixture
def controlador(qtbot):
    ventana_real = VentanaReimpresionCompras("Test", "admin", lambda: None)
    qtbot.addWidget(ventana_real)

    ventana_real.tabla.currentRow = MagicMock(return_value=0)
    mock_item = MagicMock()
    mock_item.text.return_value = "ruta/ficticia.pdf"
    ventana_real.tabla.item = MagicMock(return_value=mock_item)

    controlador = ReimpresionComprasControlador(MagicMock(), "Test", "admin")
    controlador.ventana = ventana_real
    return controlador


def test_volver_a_inicio_cierra_y_llama_main(controlador):
    mock_main = MagicMock()
    controlador.main_app = mock_main
    controlador.volver_a_inicio()
    assert not controlador.ventana.isVisible()
    mock_main.mostrar_ventana_inicio.assert_called_once()


def test_obtener_documento_seleccionado_devuelve_ruta(controlador):
    ruta = controlador.obtener_documento_seleccionado()
    assert ruta == "ruta/ficticia.pdf"


def test_obtener_documento_sin_seleccion(controlador, mocker):
    controlador.ventana.tabla.currentRow.return_value = -1
    mock_warning = mocker.patch.object(QMessageBox, "warning")
    ruta = controlador.obtener_documento_seleccionado()
    assert ruta is None
    mock_warning.assert_called_once()


def test_imprimir_documento_ok(controlador, mocker):
    mock_exists = mocker.patch("os.path.exists", return_value=True)
    mock_popen = mocker.patch("subprocess.Popen")
    mock_info = mocker.patch.object(QMessageBox, "information")

    controlador.imprimir_documento()

    mock_exists.assert_called_once()
    mock_popen.assert_called_once()
    mock_info.assert_called_once()


def test_imprimir_documento_no_existe(controlador, mocker):
    mocker.patch("os.path.exists", return_value=False)
    mock_warning = mocker.patch.object(QMessageBox, "warning")

    controlador.imprimir_documento()

    mock_warning.assert_called_once()


def test_enviar_documento_ok(controlador, mocker):
    mock_dialog = mocker.patch(
        "controladores.reimpresionCompras_controlador.VentanaCorreoConfirmacion")
    instancia_dialogo = mock_dialog.return_value
    instancia_dialogo.exec.return_value = True
    instancia_dialogo.correo_seleccionado = "cliente@correo.com"

    mock_envio = mocker.patch(
        "controladores.reimpresionCompras_controlador.enviar_correo_reimpresion_compra", return_value=(True, None))
    mock_info = mocker.patch.object(QMessageBox, "information")

    controlador.enviar_documento()

    mock_envio.assert_called_once()
    mock_info.assert_called_once()


def test_enviar_documento_falla_envio(controlador, mocker):
    mock_dialog = mocker.patch(
        "controladores.reimpresionCompras_controlador.VentanaCorreoConfirmacion")
    instancia_dialogo = mock_dialog.return_value
    instancia_dialogo.exec.return_value = True
    instancia_dialogo.correo_seleccionado = "cliente@correo.com"

    mock_envio = mocker.patch(
        "controladores.reimpresionCompras_controlador.enviar_correo_reimpresion_compra", return_value=(False, "Error SMTP"))
    mock_error = mocker.patch.object(QMessageBox, "critical")

    controlador.enviar_documento()

    mock_envio.assert_called_once()
    mock_error.assert_called_once()
