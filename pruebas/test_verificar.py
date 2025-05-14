"""
TESTS AUTOMÁTICOS: Ventana de verificación de código (VentanaVerificar)

Este módulo realiza pruebas sobre la interfaz de la pantalla donde el usuario
introduce un código de recuperación enviado por correo.

Objetivos de estas pruebas:
1. Verificar que la ventana se inicializa correctamente sin errores.
2. Asegurar que existe un botón visible y etiquetado como "Verificar".

Estas pruebas utilizan `pytest-qt` para trabajar con interfaces gráficas
(PySide6) en modo de prueba (sin necesidad de mostrar la ventana).

Dependencias:
- pytest
- pytest-qt
- PySide6
"""

import pytest
from pruebas.verificar_test import iniciar_ventana_verificar
from PySide6.QtWidgets import QPushButton

# ------------------------------------------------------------------------------
# TEST 1: Verificar que la ventana se crea correctamente
# ------------------------------------------------------------------------------


def test_ventana_verificar_se_inicializa(qtbot):
    """
    TEST: Inicialización de VentanaVerificar

    Crea una instancia de la ventana y la registra con `qtbot`
    para asegurarse de que la interfaz puede cargarse correctamente
    sin errores ni excepciones.

    Assertions:
    - La instancia de ventana no debe ser None.
    - Debe tener un título asignado.
    """
    ventana = iniciar_ventana_verificar()
    qtbot.addWidget(ventana)

    assert ventana is not None, "La ventana no se pudo crear"
    assert ventana.windowTitle() != "", "La ventana no tiene título asignado"


# ------------------------------------------------------------------------------
# TEST 2: Verificar que existe el botón "Verificar"
# ------------------------------------------------------------------------------

def test_boton_verificar_existe(qtbot):
    """
    TEST: Presencia del botón 'Verificar'

    Busca entre todos los botones (`QPushButton`) que haya en la ventana,
    y verifica que al menos uno tenga el texto "Verificar" (ignorando mayúsculas).

    Este botón es fundamental para validar el código OTP ingresado.

    Assertions:
    - Debe existir al menos un botón cuyo texto contenga "verificar"
    """
    ventana = iniciar_ventana_verificar()
    qtbot.addWidget(ventana)

    botones = ventana.findChildren(QPushButton)
    assert any(
        "verificar" in b.text().lower() for b in botones
    ), "No se encontró un botón con texto 'Verificar'"
