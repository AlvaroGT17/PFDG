"""
Pruebas unitarias para el controlador ReimpresionComprasControlador.

Este módulo verifica el comportamiento del controlador encargado de gestionar
la reimpresión de contratos de compra en el sistema ReyBoxes.

Se utilizan mocks para simular la ventana, el sistema de archivos y los cuadros
de diálogo. Las pruebas cubren tanto los casos de éxito como de error.
"""

import pytest
from unittest.mock import MagicMock, patch
from controladores.reimpresionCompras_controlador import ReimpresionComprasControlador


@pytest.fixture
def controlador(monkeypatch, qtbot):
    """
    Fixture que crea una instancia del controlador con una ventana simulada.

    Se mockea la clase VentanaReimpresionCompras y se inyecta una tabla con
    comportamiento predeterminado.

    Returns:
        ReimpresionComprasControlador: Controlador preparado para pruebas.
    """
    mock_app = MagicMock()
    mock_ventana = MagicMock()
    mock_ventana.tabla.currentRow.return_value = 0
    mock_ventana.tabla.item.return_value.text.return_value = "ruta/falsa.pdf"
    monkeypatch.setattr(
        "controladores.reimpresionCompras_controlador.VentanaReimpresionCompras",
        lambda *a, **k: mock_ventana
    )

    controlador = ReimpresionComprasControlador(mock_app, "Test", "admin")
    controlador.ventana = mock_ventana
    return controlador


def test_volver_a_inicio_cierra_y_llama_main(controlador):
    """
    Verifica que la función volver_a_inicio cierra la ventana actual y
    llama al método mostrar_ventana_inicio de la aplicación principal.
    """
    controlador.volver_a_inicio()
    controlador.ventana.close.assert_called_once()
    controlador.main_app.mostrar_ventana_inicio.assert_called_once_with(
        "Test", "admin")


def test_obtener_documento_valido(controlador):
    """
    Comprueba que obtener_documento_seleccionado devuelve la ruta del documento
    cuando hay una fila seleccionada en la tabla.
    """
    ruta = controlador.obtener_documento_seleccionado()
    assert ruta == "ruta/falsa.pdf"


def test_obtener_documento_no_valido_sin_seleccion(controlador):
    """
    Verifica que obtener_documento_seleccionado devuelve None y lanza una advertencia
    si no hay ninguna fila seleccionada.
    """
    controlador.ventana.tabla.currentRow.return_value = -1
    with patch("controladores.reimpresionCompras_controlador.QMessageBox.warning") as mock_warn:
        ruta = controlador.obtener_documento_seleccionado()
        assert ruta is None
        mock_warn.assert_called_once()


def test_imprimir_documento_ok(controlador, monkeypatch):
    """
    Verifica que imprimir_documento ejecuta correctamente subprocess.Popen
    y muestra un mensaje de éxito cuando el archivo existe.
    """
    monkeypatch.setattr("os.path.exists", lambda x: True)
    mock_popen = monkeypatch.setattr("subprocess.Popen", MagicMock())
    with patch("controladores.reimpresionCompras_controlador.QMessageBox.information") as mock_info:
        controlador.imprimir_documento()
        mock_popen.assert_called_once()
        mock_info.assert_called_once()


def test_imprimir_documento_falla(controlador, monkeypatch):
    """
    Verifica que imprimir_documento muestra un mensaje de error si ocurre
    una excepción al intentar imprimir.
    """
    monkeypatch.setattr("os.path.exists", lambda x: True)
    monkeypatch.setattr(
        "subprocess.Popen", lambda *a, **k: (_ for _ in ()
                                             ).throw(Exception("Error"))
    )
    with patch("controladores.reimpresionCompras_controlador.QMessageBox.critical") as mock_crit:
        controlador.imprimir_documento()
        mock_crit.assert_called_once()


def test_imprimir_documento_no_existe(controlador, monkeypatch):
    """
    Verifica que imprimir_documento muestra una advertencia si el archivo
    no existe físicamente.
    """
    monkeypatch.setattr("os.path.exists", lambda x: False)
    with patch("controladores.reimpresionCompras_controlador.QMessageBox.warning") as mock_warn:
        controlador.imprimir_documento()
        mock_warn.assert_called_once()


def test_imprimir_documento_ok(controlador, monkeypatch):
    """
    Verifica nuevamente el caso correcto de impresión, asegurando que
    subprocess.Popen se ejecuta sin errores y se muestra confirmación.
    """
    monkeypatch.setattr("os.path.exists", lambda x: True)
    mock_popen = MagicMock()
    monkeypatch.setattr("subprocess.Popen", mock_popen)
    with patch("controladores.reimpresionCompras_controlador.QMessageBox.information") as mock_info:
        controlador.imprimir_documento()
        mock_popen.assert_called_once()
        mock_info.assert_called_once()


def test_enviar_documento_falla(controlador, monkeypatch):
    """
    Simula un fallo al enviar un documento por correo y verifica que
    se muestra un mensaje de error correspondiente.
    """
    mock_dialog = MagicMock()
    mock_dialog.exec.return_value = True
    mock_dialog.correo_seleccionado = "cliente@ejemplo.com"

    monkeypatch.setattr(
        "controladores.reimpresionCompras_controlador.VentanaCorreoConfirmacion",
        lambda x: mock_dialog
    )
    monkeypatch.setattr(
        "controladores.reimpresionCompras_controlador.enviar_correo_reimpresion_compra",
        lambda c, r: (False, "Error grave")
    )

    with patch("controladores.reimpresionCompras_controlador.QMessageBox.critical") as mock_crit:
        controlador.enviar_documento()
        mock_crit.assert_called_once()
