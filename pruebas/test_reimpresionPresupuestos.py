import os
import pytest
import builtins
from PySide6.QtWidgets import QToolButton, QTableWidget, QTableWidgetItem, QMessageBox
from pruebas.reimpresionPresupuestos_test import iniciar_ventana_reimpresion_presupuestos


def test_reimpresion_presupuestos_componentes(qtbot):
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)
    ventana.show()

    tabla = ventana.findChild(QTableWidget)
    assert tabla is not None
    assert tabla.columnCount() == 3

    botones = ventana.findChildren(QToolButton)
    textos = [btn.text().lower() for btn in botones]

    assert any("volver" in t for t in textos)
    assert any("enviar" in t for t in textos)
    assert any("imprimir" in t for t in textos)


def test_botones_tienen_icono(qtbot):
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)

    for btn in [ventana.btn_enviar, ventana.btn_imprimir, ventana.btn_volver]:
        assert not btn.icon().isNull()


def test_tabla_configurada_correctamente(qtbot):
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)

    tabla = ventana.tabla
    assert tabla.selectionBehavior() == QTableWidget.SelectRows
    assert tabla.editTriggers() == QTableWidget.NoEditTriggers
    assert tabla.columnCount() == 3
    assert tabla.isColumnHidden(2)


def test_abrir_documento_no_existente_muestra_warning(qtbot, mocker):
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)

    ventana.tabla.setRowCount(1)
    ventana.tabla.setItem(0, 2, QTableWidgetItem("ruta/falsa/documento.pdf"))

    mock_warning = mocker.patch.object(QMessageBox, "warning")
    ventana.abrir_documento_seleccionado(0, 0)

    mock_warning.assert_called_once()
    assert "no existe" in mock_warning.call_args[0][2].lower()


def test_cargar_documentos_lee_archivos_correctamente(qtbot, tmp_path, monkeypatch):
    carpeta_mes = tmp_path / "documentos" / "presupuestos" / "abril_2025"
    carpeta_mes.mkdir(parents=True)
    archivo = carpeta_mes / "presupuesto_test.pdf"
    archivo.write_text("PDF de prueba")

    # Guardar referencia real al open original
    real_open = builtins.open

    def ruta_falsa(ruta):
        if ruta.startswith("css"):
            return "css/falso.css"
        return str(tmp_path / "documentos" / "presupuestos")

    monkeypatch.setattr(
        "vistas.ventana_reimpresionPresupuestos.obtener_ruta_absoluta",
        ruta_falsa
    )

    # Ahora monkeypatch.open apunta al open real del sistema
    monkeypatch.setattr("builtins.open", lambda *a, **
                        k: real_open(os.devnull, "r"))

    from vistas.ventana_reimpresionPresupuestos import VentanaReimpresionPresupuestos
    ventana = VentanaReimpresionPresupuestos("Usuario", "admin", lambda: None)
    qtbot.addWidget(ventana)

    assert ventana.tabla.rowCount() == 1
    assert "presupuesto_test.pdf" in ventana.tabla.item(0, 1).text().lower()
