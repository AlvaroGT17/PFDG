"""
TESTS AUTOMÁTICOS: Ventana de Reimpresión de Presupuestos

Este módulo valida el correcto funcionamiento de la ventana
`VentanaReimpresionPresupuestos`, incluyendo estructura gráfica,
interacción de botones, carga de archivos y gestión de errores.

Cobertura:
- Componentes visibles y botones funcionales.
- Estructura y configuración de la tabla.
- Comprobación de iconos presentes.
- Simulación de rutas falsas con `monkeypatch` para pruebas controladas.
- Simulación de documentos válidos e inexistentes.
- Verificación del botón "Volver".

Requiere:
- pytest
- pytest-qt
- PySide6
"""

import os
import gc
import builtins
import pytest
from unittest.mock import patch
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QToolButton, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from pruebas.reimpresionPresupuestos_test import iniciar_ventana_reimpresion_presupuestos


@pytest.fixture(autouse=True)
def cerrar_ventanas_despues_test():
    """
    Limpia todas las ventanas abiertas después de cada test para evitar fugas de memoria.
    """
    yield
    for widget in QApplication.allWidgets():
        if isinstance(widget, QWidget):
            widget.close()
            widget.deleteLater()
    QApplication.processEvents()
    gc.collect()


@pytest.fixture(autouse=True)
def evitar_mostrar_qt(monkeypatch):
    """
    Anula el método `show()` de QWidget para evitar mostrar ventanas durante los tests.
    """
    monkeypatch.setattr("PySide6.QtWidgets.QWidget.show", lambda self: None)


def test_reimpresion_presupuestos_componentes(qtbot):
    """
    TEST 1: Verifica que la ventana contiene tabla y botones principales: Enviar, Imprimir, Volver.
    """
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)

    tabla = ventana.findChild(QTableWidget)
    assert tabla is not None
    assert tabla.columnCount() == 3

    botones = ventana.findChildren(QToolButton)
    textos = [btn.text().lower() for btn in botones]

    assert any("volver" in t for t in textos)
    assert any("enviar" in t for t in textos)
    assert any("imprimir" in t for t in textos)


def test_botones_tienen_icono(qtbot):
    """
    TEST 2: Verifica que los botones tienen iconos correctamente asignados.
    """
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)

    for btn in [ventana.btn_enviar, ventana.btn_imprimir, ventana.btn_volver]:
        assert not btn.icon().isNull()


def test_tabla_configurada_correctamente(qtbot):
    """
    TEST 3: Valida que la tabla esté configurada como solo lectura y con selección de filas.
    """
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)

    tabla = ventana.tabla
    assert tabla.selectionBehavior() == QTableWidget.SelectRows
    assert tabla.editTriggers() == QTableWidget.NoEditTriggers
    assert tabla.columnCount() == 3
    assert tabla.isColumnHidden(2)


def test_abrir_documento_no_existente_muestra_warning(qtbot, mocker):
    """
    TEST 4: Intenta abrir un archivo inexistente y verifica que se muestre una advertencia.
    """
    ventana = iniciar_ventana_reimpresion_presupuestos()
    qtbot.addWidget(ventana)

    ventana.tabla.setRowCount(1)
    ventana.tabla.setItem(0, 2, QTableWidgetItem("ruta/falsa/documento.pdf"))

    mock_warning = mocker.patch.object(QMessageBox, "warning")
    ventana.abrir_documento_seleccionado(0, 0)

    mock_warning.assert_called_once()
    assert "no existe" in mock_warning.call_args[0][2].lower()


def test_cargar_documentos_lee_archivos_correctamente(qtbot, tmp_path, monkeypatch):
    """
    TEST 5: Crea un archivo temporal y verifica que la ventana lo carga correctamente.
    """
    carpeta_mes = tmp_path / "documentos" / "presupuestos" / "abril_2025"
    carpeta_mes.mkdir(parents=True)
    archivo = carpeta_mes / "presupuesto_test.pdf"
    archivo.write_text("PDF de prueba")

    real_open = builtins.open  # evitar errores por monkeypatching global

    monkeypatch.setattr(
        "vistas.ventana_reimpresionPresupuestos.obtener_ruta_absoluta",
        lambda ruta: str(tmp_path / "documentos" / "presupuestos")
    )
    monkeypatch.setattr("builtins.open", lambda *a, **
                        k: real_open(os.devnull, "r"))

    from vistas.ventana_reimpresionPresupuestos import VentanaReimpresionPresupuestos
    ventana = VentanaReimpresionPresupuestos("Usuario", "admin", lambda: None)
    qtbot.addWidget(ventana)

    assert ventana.tabla.rowCount() == 1
    assert "presupuesto_test.pdf" in ventana.tabla.item(0, 1).text().lower()


def test_boton_volver_ejecuta_callback(qtbot):
    """
    TEST 6: Comprueba que al pulsar 'Volver' se ejecuta el callback correspondiente.
    """
    llamado = {"valor": False}

    def callback():
        llamado["valor"] = True

    from vistas.ventana_reimpresionPresupuestos import VentanaReimpresionPresupuestos
    ventana = VentanaReimpresionPresupuestos("Usuario", "admin", callback)
    qtbot.addWidget(ventana)

    qtbot.mouseClick(ventana.btn_volver, Qt.LeftButton)

    assert llamado["valor"] is True, "El callback del botón 'Volver' no se ejecutó"
