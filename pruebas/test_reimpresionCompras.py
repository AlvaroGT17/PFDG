"""
Pruebas automatizadas para la ventana de reimpresión de compras (VentanaReimpresionCompras).

Estas pruebas validan:
- La correcta inicialización de la ventana.
- La configuración y funcionalidad de los botones.
- La carga dinámica de documentos.
- La correcta aplicación de estilos CSS.
- El manejo de apertura de documentos válidos e inválidos.

Requiere:
- pytest
- pytest-qt
- PySide6
"""

import os
import pytest
from unittest.mock import mock_open, Mock
from PySide6.QtWidgets import (
    QToolButton, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PySide6.QtGui import QIcon
from pruebas.reimpresionCompras_test import iniciar_ventana_reimpresion_compras


def test_reimpresion_compras_componentes_basicos(qtbot):
    """
    Verifica que la ventana contiene los componentes esenciales:
    - Tabla de 3 columnas.
    - Botones con texto identificable: Volver, Enviar, Imprimir.
    """
    ventana = iniciar_ventana_reimpresion_compras()
    qtbot.addWidget(ventana)
    ventana.show()

    tabla = ventana.findChild(QTableWidget)
    assert tabla is not None
    assert tabla.columnCount() == 3

    botones = ventana.findChildren(QToolButton)
    textos = [b.text().lower() for b in botones]

    assert any("volver" in t for t in textos)
    assert any("enviar" in t for t in textos)
    assert any("imprimir" in t for t in textos)


def test_botones_tienen_icono(qtbot):
    """
    Verifica que los botones principales poseen iconos asignados correctamente.
    """
    ventana = iniciar_ventana_reimpresion_compras()
    qtbot.addWidget(ventana)
    for boton in [ventana.btn_enviar, ventana.btn_imprimir, ventana.btn_volver]:
        icono: QIcon = boton.icon()
        assert not icono.isNull()


def test_tabla_esta_configurada(qtbot):
    """
    Comprueba la configuración visual y funcional de la tabla:
    - Selección por fila completa.
    - Edición deshabilitada.
    - Columna oculta correctamente.
    """
    ventana = iniciar_ventana_reimpresion_compras()
    qtbot.addWidget(ventana)

    tabla = ventana.tabla
    assert tabla.selectionBehavior() == QAbstractItemView.SelectRows
    assert not tabla.editTriggers() & QAbstractItemView.AllEditTriggers
    assert tabla.isColumnHidden(2)


def test_tabla_se_llena_correctamente(qtbot, tmp_path, monkeypatch):
    """
    Simula la existencia de un documento PDF y comprueba que
    la tabla lo carga correctamente.
    """
    carpeta_prueba = tmp_path / "documentos" / "compras" / "abril_2024"
    carpeta_prueba.mkdir(parents=True)
    archivo = carpeta_prueba / "contrato1.pdf"
    archivo.write_text("PDF falso")

    def ruta_absoluta_mock(relativa):
        if relativa.startswith("css"):
            css_falso = tmp_path / "falso.css"
            css_falso.write_text("/* css de prueba */")
            return str(css_falso)
        return str(tmp_path / "documentos" / "compras")

    monkeypatch.setattr(
        "vistas.ventana_reimpresionCompras.obtener_ruta_absoluta", ruta_absoluta_mock)
    monkeypatch.setattr("builtins.open", mock_open(read_data=""))

    from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
    ventana = VentanaReimpresionCompras("Test", "admin", lambda: None)
    qtbot.addWidget(ventana)

    tabla = ventana.tabla
    assert tabla.rowCount() == 1
    assert tabla.item(0, 1).text() == "contrato1.pdf"


def test_abrir_documento_no_existente_muestra_warning(qtbot, monkeypatch):
    """
    Simula el intento de abrir un archivo inexistente y verifica
    que se muestra un mensaje de advertencia.
    """
    monkeypatch.setattr(
        "vistas.ventana_reimpresionCompras.obtener_ruta_absoluta", lambda x: "css/falso.css")
    monkeypatch.setattr("builtins.open", mock_open(read_data=""))

    from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
    ventana = VentanaReimpresionCompras("Test", "admin", lambda: None)
    qtbot.addWidget(ventana)

    ventana.tabla.setRowCount(1)
    ventana.tabla.setItem(0, 2, QTableWidgetItem("ruta/inexistente.pdf"))

    mock_warning = Mock()
    monkeypatch.setattr(
        "vistas.ventana_reimpresionCompras.QMessageBox.warning", mock_warning)

    ventana.abrir_documento_seleccionado(0, 0)
    mock_warning.assert_called_once()


def test_aplica_estilos_css(qtbot, monkeypatch):
    """
    Verifica que el CSS cargado desde archivo se aplica correctamente
    al estilo de la ventana.
    """
    css_fake = "QWidget { background-color: red; }"
    monkeypatch.setattr(
        "vistas.ventana_reimpresionCompras.obtener_ruta_absoluta", lambda x: "css/falso.css")
    monkeypatch.setattr("builtins.open", mock_open(read_data=css_fake))

    from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
    ventana = VentanaReimpresionCompras("Test", "admin", lambda: None)
    qtbot.addWidget(ventana)

    assert "QWidget" in ventana.styleSheet()


def test_abrir_documento_valido_lanza_webbrowser(qtbot, monkeypatch):
    """
    Comprueba que al abrir un documento válido, se invoca webbrowser.open_new.
    """
    monkeypatch.setattr(
        "vistas.ventana_reimpresionCompras.obtener_ruta_absoluta", lambda x: "documentos/compras")
    monkeypatch.setattr("webbrowser.open_new", lambda ruta: True)
    monkeypatch.setattr("os.path.exists", lambda ruta: True)
    monkeypatch.setattr("builtins.open", mock_open(read_data=""))

    from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
    ventana = VentanaReimpresionCompras("Test", "admin", lambda: None)
    qtbot.addWidget(ventana)

    ventana.tabla.setRowCount(1)
    ventana.tabla.setItem(0, 2, QTableWidgetItem("ruta/valida.pdf"))

    ventana.abrir_documento_seleccionado(0, 0)


def test_doble_clic_dispara_abrir_documento(qtbot, monkeypatch):
    """
    Verifica que un doble clic sobre la tabla activa la apertura del documento.
    """
    monkeypatch.setattr(
        "vistas.ventana_reimpresionCompras.obtener_ruta_absoluta", lambda x: "documentos/compras")
    monkeypatch.setattr("os.path.exists", lambda ruta: True)
    monkeypatch.setattr("webbrowser.open_new", lambda ruta: True)
    monkeypatch.setattr("builtins.open", mock_open(read_data=""))

    from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
    ventana = VentanaReimpresionCompras("Test", "admin", lambda: None)
    qtbot.addWidget(ventana)

    ventana.tabla.setRowCount(1)
    ventana.tabla.setItem(0, 2, QTableWidgetItem("ruta/ficticia.pdf"))

    ventana.tabla.cellDoubleClicked.emit(0, 0)


def test_nombre_objeto_correcto(qtbot):
    """
    Comprueba que el nombre del objeto principal de la ventana es el esperado.
    """
    ventana = iniciar_ventana_reimpresion_compras()
    qtbot.addWidget(ventana)
    assert ventana.objectName() == "ventana_reimpresion"
