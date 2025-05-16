# pruebas/test_reimpresion_presupuestos_controlador.py
# ─────────────────────────────────────────────────────

import pytest
import os
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QTableWidgetItem
from controladores.reimpresionPresupuestos_controlador import ReimpresionPresupuestosControlador


@pytest.fixture
def controlador():
    with patch("controladores.reimpresionPresupuestos_controlador.VentanaReimpresionPresupuestos") as MockVentana:
        ventana_mock = MockVentana.return_value
        ventana_mock.tabla.currentRow.return_value = 0
        ventana_mock.tabla.item.return_value = QTableWidgetItem(
            "ruta/ficticia.pdf")
        main_app_mock = MagicMock()
        return ReimpresionPresupuestosControlador(main_app_mock, "Cresnik", "admin")


def test_volver_a_inicio_cierra_y_llama_main(controlador):
    controlador.volver_a_inicio()
    controlador.main_app.mostrar_ventana_inicio.assert_called_once_with(
        "Cresnik", "admin")


def test_obtener_documento_valido(controlador):
    with patch("os.path.exists", return_value=True):
        ruta = controlador.obtener_documento_seleccionado()
        assert ruta == "ruta/ficticia.pdf"


def test_obtener_documento_no_valido(controlador):
    with patch("os.path.exists", return_value=False):
        ruta = controlador.obtener_documento_seleccionado()
        assert ruta is None


def test_imprimir_documento_ok(controlador):
    with patch("os.path.exists", return_value=True), \
            patch("webbrowser.open_new") as mock_browser:
        controlador.imprimir_documento()
        mock_browser.assert_called_once_with("ruta/ficticia.pdf")


def test_imprimir_documento_falla(controlador):
    with patch("os.path.exists", return_value=True), \
            patch("webbrowser.open_new", side_effect=Exception("fallo")), \
            patch("PySide6.QtWidgets.QMessageBox.critical") as mock_msg:
        controlador.imprimir_documento()
        mock_msg.assert_called_once()


def test_enviar_documento_exito(controlador):
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
    with patch("os.path.exists", return_value=True), \
            patch("controladores.reimpresionPresupuestos_controlador.VentanaCorreoConfirmacion") as MockDialogo, \
            patch("controladores.reimpresionPresupuestos_controlador.enviar_correo_presupuesto", return_value=(False, "Error")), \
            patch("PySide6.QtWidgets.QMessageBox.critical") as mock_crit:
        dialogo = MockDialogo.return_value
        dialogo.exec.return_value = True
        dialogo.correo_seleccionado = "cliente@correo.com"
        controlador.enviar_documento()
        mock_crit.assert_called_once()
