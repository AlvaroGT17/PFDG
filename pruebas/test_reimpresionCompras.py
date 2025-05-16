import os
import pytest
from PySide6.QtWidgets import (
    QToolButton, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PySide6.QtGui import QIcon
from pruebas.reimpresionCompras_test import iniciar_ventana_reimpresion_compras


def test_reimpresion_compras_componentes_basicos(qtbot):
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
    ventana = iniciar_ventana_reimpresion_compras()
    qtbot.addWidget(ventana)
    for boton in [ventana.btn_enviar, ventana.btn_imprimir, ventana.btn_volver]:
        icono: QIcon = boton.icon()
        assert not icono.isNull()


def test_tabla_esta_configurada(qtbot):
    ventana = iniciar_ventana_reimpresion_compras()
    qtbot.addWidget(ventana)

    tabla = ventana.tabla
    assert tabla.selectionBehavior() == QAbstractItemView.SelectRows
    assert not tabla.editTriggers() & QAbstractItemView.AllEditTriggers
    assert tabla.isColumnHidden(2)


def test_tabla_se_llena_correctamente(qtbot, tmp_path, monkeypatch):
    carpeta_prueba = tmp_path / "documentos" / "compras" / "abril_2024"
    carpeta_prueba.mkdir(parents=True)
    archivo = carpeta_prueba / "contrato1.pdf"
    archivo.write_text("PDF falso")

    def ruta_absoluta_mock(relativa):
        if relativa.startswith("css"):
            # Devuelve una ruta a un archivo CSS ficticio válido
            css_falso = tmp_path / "falso.css"
            css_falso.write_text("/* css de prueba */")
            return str(css_falso)
        return str(tmp_path / "documentos" / "compras")

    monkeypatch.setattr(
        "vistas.ventana_reimpresionCompras.obtener_ruta_absoluta",
        ruta_absoluta_mock
    )

    from vistas.ventana_reimpresionCompras import VentanaReimpresionCompras
    ventana = VentanaReimpresionCompras("Test", "admin", lambda: None)
    qtbot.addWidget(ventana)

    tabla = ventana.tabla
    assert tabla.rowCount() == 1
    assert tabla.item(0, 1).text() == "contrato1.pdf"


def test_abrir_documento_no_existente_muestra_warning(qtbot, mocker):
    ventana = iniciar_ventana_reimpresion_compras()
    qtbot.addWidget(ventana)

    ventana.tabla.setRowCount(1)
    ventana.tabla.setItem(0, 2, QTableWidgetItem("ruta/inexistente.pdf"))

    mock_warning = mocker.patch(
        "vistas.ventana_reimpresionCompras.QMessageBox.warning"
    )

    ventana.abrir_documento_seleccionado(0, 0)

    mock_warning.assert_called_once()
