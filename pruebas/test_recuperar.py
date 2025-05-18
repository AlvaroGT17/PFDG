"""
Pruebas automáticas para la ventana de recuperación de cuenta.

Este módulo valida el correcto funcionamiento de la ventana `VentanaRecuperar`,
incluyendo:

- Título de la ventana.
- Presencia y comportamiento de campos y botones.
- Validación de entrada y activación de botones.
- Estilos visuales y tooltips definidos.

Requiere:
- pytest
- pytest-qt
- PySide6
"""

import pytest
from PySide6.QtWidgets import QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
from pruebas.recuperar_test import iniciar_ventana_recuperar


def test_ventana_tiene_titulo_correcto(qtbot):
    """
    Verifica que el título de la ventana contiene la palabra 'Recuperar'.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "Recuperar" in ventana.windowTitle()


def test_recuperar_campos_y_botones(qtbot):
    """
    Comprueba que:
    - El campo de correo existe y tiene el placeholder correcto.
    - Existen botones de enviar y volver con sus respectivos textos.
    """
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
    """
    Verifica que el botón 'Enviar' está desactivado si el campo está vacío.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    ventana.input_correo.setText("")
    assert not ventana.btn_enviar.isEnabled()


def test_boton_enviar_inactivo_por_defecto(qtbot):
    """
    Verifica que al iniciar la ventana, el botón 'Enviar' está desactivado.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert not ventana.btn_enviar.isEnabled()


def test_boton_volver_esta_presente(qtbot):
    """
    Comprueba que el botón 'Volver' está presente y tiene el texto adecuado.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "volver" in ventana.btn_volver.text().lower()


def test_icono_correo_presente(qtbot):
    """
    Verifica que el icono correspondiente al campo de correo está presente.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    icono = ventana.findChildren(QLabel)[1]
    assert icono.pixmap() is not None


def test_css_aplicado_correctamente(qtbot):
    """
    Comprueba que el archivo CSS ha sido aplicado correctamente.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert ventana.styleSheet() != ""


def test_tooltip_campo_correo_definido(qtbot):
    """
    Verifica que el campo de correo tiene un tooltip explicativo.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "correo" in ventana.input_correo.toolTip().lower()


def test_tooltip_boton_enviar_definido(qtbot):
    """
    Comprueba que el botón 'Enviar' tiene un tooltip que menciona el código.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "código" in ventana.btn_enviar.toolTip().lower()


def test_tooltip_boton_volver_definido(qtbot):
    """
    Verifica que el botón 'Volver' tiene un tooltip que hace referencia al inicio.
    """
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    assert "inicio" in ventana.btn_volver.toolTip().lower()
