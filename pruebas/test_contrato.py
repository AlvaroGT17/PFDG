import os
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot
from vistas.ventana_contrato import VentanaContrato
from PySide6.QtWidgets import QPushButton, QTextBrowser
from pruebas.contrato_test import iniciar_ventana_contrato


def iniciar_ventana_contrato(callback_aceptar=None):
    html_path = os.path.join(os.path.dirname(__file__), "contrato_test.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("<html><body><h1>Contrato de Venta</h1><p>Contenido</p></body></html>")

    return VentanaContrato(html_path, tipo_operacion="venta", callback_aceptar=callback_aceptar)


def test_contrato_ventana_visible(qtbot: QtBot):
    ventana = iniciar_ventana_contrato()
    qtbot.addWidget(ventana)
    ventana.show()
    assert ventana.isVisible()


def test_contrato_titulo_o_contenido_visible(qtbot: QtBot):
    ventana = iniciar_ventana_contrato()
    qtbot.addWidget(ventana)
    ventana.show()

    visor = ventana.findChild(QTextBrowser)
    assert visor is not None
    assert "Contrato" in visor.toPlainText()


def test_contrato_titulo_ventana_correcto(qtbot: QtBot):
    ventana = iniciar_ventana_contrato()
    assert ventana.windowTitle().startswith("Contrato de ")


def test_botones_estan_presentes(qtbot: QtBot):
    ventana = iniciar_ventana_contrato()
    botones = ventana.findChildren(QPushButton)
    boton_volver = next((b for b in botones if b.text() == "Volver"), None)
    boton_aceptar = ventana.findChild(QPushButton, "boton_aceptar_contrato")

    assert boton_volver is not None
    assert boton_aceptar is not None
    assert boton_aceptar.text() == "Aceptar contrato"


def test_tooltips_botones(qtbot: QtBot):
    ventana = iniciar_ventana_contrato()
    botones = ventana.findChildren(QPushButton)
    boton_volver = next((b for b in botones if b.text() == "Volver"), None)
    boton_aceptar = ventana.findChild(QPushButton, "boton_aceptar_contrato")

    assert boton_volver.toolTip() == "Volver sin aceptar el contrato"
    assert boton_aceptar.toolTip(
    ) == "Aceptar el contrato y continuar con las acciones seleccionadas"


def test_callback_se_ejecuta(qtbot: QtBot):
    llamado = {"valor": None}

    def callback(tipo):
        llamado["valor"] = tipo

    ventana = iniciar_ventana_contrato(callback_aceptar=callback)
    qtbot.addWidget(ventana)
    ventana.show()

    boton_aceptar = ventana.findChild(QPushButton, "boton_aceptar_contrato")
    qtbot.mouseClick(boton_aceptar, Qt.LeftButton)

    assert llamado["valor"] == "venta"
