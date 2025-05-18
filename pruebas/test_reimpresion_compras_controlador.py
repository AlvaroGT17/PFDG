"""
Pruebas unitarias para el controlador ReimpresionComprasControlador.

Este módulo comprueba:

- Navegación al menú principal.
- Obtención correcta de documentos seleccionados.
- Impresión de archivos existentes y manejo de errores.
- Envío por correo electrónico con control de diálogos y respuestas.
- Gestión de errores y mensajes al usuario.

Dependencias:
- pytest
- unittest.mock
- PySide6
"""

import pytest
from unittest.mock import patch, MagicMock
from controladores.reimpresionCompras_controlador import ReimpresionComprasControlador
from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
from PySide6.QtWidgets import QMessageBox


@pytest.fixture
def controlador(qtbot):
    """
    Fixture que proporciona un controlador con su ventana real,
    parcialmente mockeada para pruebas unitarias.
    """
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
    """
    Verifica que al invocar volver_a_inicio:
    - Se cierra la ventana.
    - Se llama al método mostrar_ventana_inicio del main_app.
    """
    mock_main = MagicMock()
    controlador.main_app = mock_main
    controlador.volver_a_inicio()
    assert not controlador.ventana.isVisible()
    mock_main.mostrar_ventana_inicio.assert_called_once()


def test_obtener_documento_seleccionado_devuelve_ruta(controlador):
    """
    Comprueba que se obtiene correctamente la ruta del documento seleccionado.
    """
    ruta = controlador.obtener_documento_seleccionado()
    assert ruta == "ruta/ficticia.pdf"


def test_obtener_documento_sin_seleccion(controlador, mocker):
    """
    Si no hay fila seleccionada, la función debe devolver None y mostrar advertencia.
    """
    controlador.ventana.tabla.currentRow.return_value = -1
    mock_warning = mocker.patch.object(QMessageBox, "warning")
    ruta = controlador.obtener_documento_seleccionado()
    assert ruta is None
    mock_warning.assert_called_once()


def test_imprimir_documento_ok(controlador, mocker):
    """
    Verifica que se imprime un documento existente correctamente
    usando subprocess.Popen y se informa al usuario.
    """
    mock_exists = mocker.patch("os.path.exists", return_value=True)
    mock_popen = mocker.patch("subprocess.Popen")
    mock_info = mocker.patch.object(QMessageBox, "information")

    controlador.imprimir_documento()

    mock_exists.assert_called_once()
    mock_popen.assert_called_once()
    mock_info.assert_called_once()


def test_imprimir_documento_no_existe(controlador, mocker):
    """
    Verifica que si el archivo no existe, se muestra un mensaje de advertencia.
    """
    mocker.patch("os.path.exists", return_value=False)
    mock_warning = mocker.patch.object(QMessageBox, "warning")

    controlador.imprimir_documento()

    mock_warning.assert_called_once()


def test_enviar_documento_ok(controlador, mocker):
    """
    Simula el envío exitoso de un correo de reimpresión y verifica que:
    - Se llama a la función de envío.
    - Se muestra mensaje de confirmación.
    """
    mock_dialog = mocker.patch(
        "controladores.reimpresionCompras_controlador.VentanaCorreoConfirmacion")
    instancia_dialogo = mock_dialog.return_value
    instancia_dialogo.exec.return_value = True
    instancia_dialogo.correo_seleccionado = "cliente@correo.com"

    mock_envio = mocker.patch(
        "controladores.reimpresionCompras_controlador.enviar_correo_reimpresion_compra",
        return_value=(True, None))
    mock_info = mocker.patch.object(QMessageBox, "information")

    controlador.enviar_documento()

    mock_envio.assert_called_once()
    mock_info.assert_called_once()


def test_enviar_documento_falla_envio(controlador, mocker):
    """
    Simula un fallo en el envío del correo de reimpresión y
    verifica que se muestra un mensaje de error.
    """
    mock_dialog = mocker.patch(
        "controladores.reimpresionCompras_controlador.VentanaCorreoConfirmacion")
    instancia_dialogo = mock_dialog.return_value
    instancia_dialogo.exec.return_value = True
    instancia_dialogo.correo_seleccionado = "cliente@correo.com"

    mock_envio = mocker.patch(
        "controladores.reimpresionCompras_controlador.enviar_correo_reimpresion_compra",
        return_value=(False, "Error SMTP"))
    mock_error = mocker.patch.object(QMessageBox, "critical")

    controlador.enviar_documento()

    mock_envio.assert_called_once()
    mock_error.assert_called_once()
