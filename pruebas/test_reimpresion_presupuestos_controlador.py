"""
Pruebas unitarias para el controlador ReimpresionPresupuestosControlador.

Estas pruebas aseguran:
- El correcto funcionamiento de la navegación al menú principal.
- La obtención válida de documentos seleccionados en la tabla.
- El manejo de errores al imprimir o enviar presupuestos.
- El correcto uso de diálogos y llamadas a funciones externas.

Requiere:
- pytest
- unittest.mock
- PySide6
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QTableWidgetItem
from controladores.reimpresionPresupuestos_controlador import ReimpresionPresupuestosControlador


@pytest.fixture
def controlador():
    """
    Crea una instancia simulada del controlador con su ventana mockeada.
    """
    with patch("controladores.reimpresionPresupuestos_controlador.VentanaReimpresionPresupuestos") as MockVentana:
        ventana_mock = MockVentana.return_value
        ventana_mock.tabla.currentRow.return_value = 0
        ventana_mock.tabla.item.return_value = QTableWidgetItem(
            "ruta/ficticia.pdf")
        main_app_mock = MagicMock()
        return ReimpresionPresupuestosControlador(main_app_mock, "Cresnik", "admin")


def test_volver_a_inicio_cierra_y_llama_main(controlador):
    """
    Verifica que al volver a inicio se cierra la ventana actual y se llama al método
    mostrar_ventana_inicio del main_app con los parámetros correctos.
    """
    controlador.volver_a_inicio()
    controlador.main_app.mostrar_ventana_inicio.assert_called_once_with(
        "Cresnik", "admin")


def test_obtener_documento_valido(controlador):
    """
    Verifica que se devuelve correctamente la ruta del documento si este existe en disco.
    """
    with patch("os.path.exists", return_value=True):
        ruta = controlador.obtener_documento_seleccionado()
        assert ruta == "ruta/ficticia.pdf"


def test_obtener_documento_no_valido(controlador):
    """
    Verifica que se retorna None si el documento seleccionado no existe en el sistema de archivos.
    """
    with patch("os.path.exists", return_value=False):
        ruta = controlador.obtener_documento_seleccionado()
        assert ruta is None


def test_imprimir_documento_ok(controlador):
    """
    Verifica que si el documento existe, se lanza correctamente el visor PDF por navegador.
    """
    with patch("os.path.exists", return_value=True), \
            patch("webbrowser.open_new") as mock_browser:
        controlador.imprimir_documento()
        mock_browser.assert_called_once_with("ruta/ficticia.pdf")


def test_imprimir_documento_falla(controlador):
    """
    Simula un fallo al intentar abrir el documento y verifica que se muestra
    un mensaje crítico al usuario.
    """
    with patch("os.path.exists", return_value=True), \
            patch("webbrowser.open_new", side_effect=Exception("fallo")), \
            patch("PySide6.QtWidgets.QMessageBox.critical") as mock_msg:
        controlador.imprimir_documento()
        mock_msg.assert_called_once()


def test_enviar_documento_exito(controlador):
    """
    Simula el envío exitoso del presupuesto por correo y verifica que se muestra
    un mensaje de éxito al usuario.
    """
    with patch("os.path.exists", return_value=True), \
            patch("controladores.reimpresionPresupuestos_controlador.VentanaCorreoConfirmacion") as MockDialogo, \
            patch("controladores.reimpresionPresupuestos_controlador.enviar_correo_presupuesto", return_value=(True, None)), \
            patch("PySide6.QtWidgets.QMessageBox.information") as mock_info:
        dialogo = MockDialogo.return_value
        dialogo.exec.return_value = True
        dialogo.correo_seleccionado = "cliente@correo.com"
        controlador.enviar_documento()
        mock_info.assert_called_once()


def test_enviar_documento_falla(controlador):
    """
    Simula un fallo en el envío del presupuesto por correo y verifica que se muestra
    un mensaje crítico al usuario.
    """
    with patch("os.path.exists", return_value=True), \
            patch("controladores.reimpresionPresupuestos_controlador.VentanaCorreoConfirmacion") as MockDialogo, \
            patch("controladores.reimpresionPresupuestos_controlador.enviar_correo_presupuesto", return_value=(False, "Error")), \
            patch("PySide6.QtWidgets.QMessageBox.critical") as mock_crit:
        dialogo = MockDialogo.return_value
        dialogo.exec.return_value = True
        dialogo.correo_seleccionado = "cliente@correo.com"
        controlador.enviar_documento()
        mock_crit.assert_called_once()
