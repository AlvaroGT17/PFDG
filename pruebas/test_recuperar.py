import pytest
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
from pruebas.recuperar_test import iniciar_ventana_recuperar


def test_ventana_tiene_titulo_correcto(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "Recuperar" in ventana.windowTitle()


def test_recuperar_campos_y_botones(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    campo = ventana.findChild(QLineEdit)
    assert campo is not None
    assert campo.placeholderText() == "Introduce tu correo..."

    botones = ventana.findChildren(QPushButton)
    textos = [btn.text().lower() for btn in botones]
    assert any("enviar" in texto for texto in textos)
    assert any("volver" in texto for texto in textos)


def test_boton_enviar_inactivo_si_vacio(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    ventana.input_correo.setText("")
    assert not ventana.btn_enviar.isEnabled()


def test_boton_enviar_inactivo_por_defecto(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert not ventana.btn_enviar.isEnabled()


# Este test solo es útil si conectas validación en tiempo real
# def test_boton_enviar_activo_si_correo_valido(qtbot):
#     ventana = iniciar_ventana_recuperar()
#     qtbot.addWidget(ventana)
#     ventana.input_correo.setText("usuario@correo.com")
#     ventana.input_correo.textChanged.emit("usuario@correo.com")
#     assert ventana.btn_enviar.isEnabled()


def test_boton_volver_esta_presente(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "volver" in ventana.btn_volver.text().lower()


def test_icono_correo_presente(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    icono = ventana.findChildren(QLabel)[1]
    assert icono.pixmap() is not None


def test_css_aplicado_correctamente(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert ventana.styleSheet() != ""


def test_tooltip_campo_correo_definido(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "correo" in ventana.input_correo.toolTip().lower()


def test_tooltip_boton_enviar_definido(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "código" in ventana.btn_enviar.toolTip().lower()


def test_tooltip_boton_volver_definido(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "inicio" in ventana.btn_volver.toolTip().lower()
