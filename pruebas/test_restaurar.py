"""
TESTS AUTOMÁTICOS: Ventana de restablecimiento de contraseña (`VentanaRestaurar`)

Este módulo realiza pruebas automatizadas sobre la interfaz gráfica donde el usuario
establece una nueva contraseña tras verificar un código OTP.

Pruebas incluidas:
- Verificación de componentes básicos (campos y botones).
- Comprobación de configuración visual (tooltips, modo de entrada, cursores).
- Validación de presencia de iconos y comportamiento esperado.

Dependencias:
- pytest
- pytest-qt
- PySide6
"""

import pytest
from PySide6.QtWidgets import QLineEdit, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QIcon
from pruebas.restaurar_test import iniciar_ventana_restaurar


def test_restaurar_componentes_basicos(qtbot):
    """
    TEST 1: Componentes esenciales de la ventana

    Comprueba que:
    - Existen al menos dos campos de entrada.
    - Los placeholders contienen "nueva contraseña" y "repetir contraseña".
    - Existen botones con texto que contenga "Guardar" y "Volver".
    """
    ventana = iniciar_ventana_restaurar()
    qtbot.addWidget(ventana)
    ventana.show()

    campos = ventana.findChildren(QLineEdit)
    assert len(campos) >= 2
    assert campos[0].placeholderText().lower() == "nueva contraseña"
    assert campos[1].placeholderText().lower() == "repetir contraseña"

    botones = ventana.findChildren(QPushButton)
    textos_botones = [btn.text().lower() for btn in botones]

    assert any(
        "guardar" in texto for texto in textos_botones), "Falta botón 'Guardar'"
    assert any(
        "volver" in texto for texto in textos_botones), "Falta botón 'Volver'"


def test_campos_password_y_tooltips(qtbot):
    """
    TEST 2: Validación de campos de contraseña

    Comprueba que:
    - Ambos campos usan modo `QLineEdit.Password` para ocultar caracteres.
    - Los tooltips contienen textos informativos relevantes.
    """
    ventana = iniciar_ventana_restaurar()
    qtbot.addWidget(ventana)

    assert ventana.input_nueva.echoMode() == QLineEdit.Password
    assert ventana.input_repetir.echoMode() == QLineEdit.Password

    assert "nueva contraseña" in ventana.input_nueva.toolTip().lower()
    assert "vuelve a escribir" in ventana.input_repetir.toolTip().lower()


def test_botones_tienen_iconos(qtbot):
    """
    TEST 3: Iconos en botones

    Verifica que los botones 'Guardar' y 'Volver' tienen asignado un objeto `QIcon`.
    """
    ventana = iniciar_ventana_restaurar()
    qtbot.addWidget(ventana)

    assert isinstance(ventana.btn_guardar.icon(),
                      QIcon), "Falta icono en botón 'Guardar'"
    assert isinstance(ventana.btn_volver.icon(),
                      QIcon), "Falta icono en botón 'Volver'"


def test_botones_tienen_cursor_correcto(qtbot):
    """
    TEST 4: Validación de cursores en botones

    Verifica que el cursor de los botones 'Guardar' y 'Volver' sea de tipo `PointingHandCursor`.
    """
    ventana = iniciar_ventana_restaurar()
    qtbot.addWidget(ventana)

    assert ventana.btn_guardar.cursor().shape() == Qt.PointingHandCursor
    assert ventana.btn_volver.cursor().shape() == Qt.PointingHandCursor
