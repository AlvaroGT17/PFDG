"""
TESTS AUTOMÁTICOS: Ventana de restablecimiento de contraseña (`VentanaRestaurar`)

Este módulo contiene pruebas automatizadas para verificar los elementos esenciales
de la ventana de restablecimiento de contraseña del sistema ReyBoxes.

Objetivos:
- Verificar que los campos de entrada están correctamente configurados.
- Asegurar que los botones tienen texto, iconos y cursores adecuados.
- Confirmar que los `tooltips` ayudan al usuario a introducir datos correctamente.

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
    TEST: Componentes visibles básicos en la ventana de restablecimiento

    Verifica que existan al menos dos campos de contraseña y botones con texto adecuado.

    Assertions:
    - Debe haber al menos 2 `QLineEdit` para contraseñas.
    - Uno debe tener placeholder "Nueva contraseña".
    - Otro debe tener placeholder "Repetir contraseña".
    - Debe haber botones con texto "Guardar" y "Volver".
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
        "guardar" in texto for texto in textos_botones), "No se encontró el botón Guardar"
    assert any(
        "volver" in texto for texto in textos_botones), "No se encontró el botón Volver"


def test_campos_password_y_tooltips(qtbot):
    """
    TEST: Configuración correcta de los campos de contraseña

    Verifica que:
    - Los campos tengan el modo oculto (`Password`).
    - Los tooltips sean informativos.

    Assertions:
    - Ambos campos deben estar en modo `QLineEdit.Password`.
    - Los tooltips deben contener información útil.
    """
    ventana = iniciar_ventana_restaurar()
    qtbot.addWidget(ventana)

    assert ventana.input_nueva.echoMode() == QLineEdit.Password
    assert ventana.input_repetir.echoMode() == QLineEdit.Password

    assert "nueva contraseña" in ventana.input_nueva.toolTip().lower()
    assert "vuelve a escribir" in ventana.input_repetir.toolTip().lower()


def test_botones_tienen_iconos(qtbot):
    """
    TEST: Verifica que los botones principales tengan iconos asignados

    Assertions:
    - Los botones Guardar y Volver deben tener iconos (`QIcon`) válidos.
    """
    ventana = iniciar_ventana_restaurar()
    qtbot.addWidget(ventana)

    assert isinstance(ventana.btn_guardar.icon(), QIcon)
    assert isinstance(ventana.btn_volver.icon(), QIcon)


def test_botones_tienen_cursor_correcto(qtbot):
    """
    TEST: Verifica que los botones tengan el cursor tipo `PointingHandCursor`.

    Esto ayuda a mejorar la experiencia de usuario y accesibilidad.

    Assertions:
    - El cursor de ambos botones debe ser `Qt.PointingHandCursor`.
    """
    ventana = iniciar_ventana_restaurar()
    qtbot.addWidget(ventana)

    assert ventana.btn_guardar.cursor().shape() == Qt.PointingHandCursor
    assert ventana.btn_volver.cursor().shape() == Qt.PointingHandCursor
