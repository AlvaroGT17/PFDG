"""
TEST UNITARIO: Controlador de verificación de código OTP (`verificar_controlador.py`).

Este test no evalúa la lógica de validación del código en sí, sino que garantiza que
la ventana de verificación (`VentanaVerificar`) se construye correctamente
y contiene los elementos básicos para funcionar.

Se utiliza `pytest-qt` para simular el entorno gráfico sin necesidad de mostrar la interfaz.
"""

import pytest
from pruebas.verificar_test import iniciar_ventana_verificar


def test_controlador_verificacion_crea_ventana(qtbot):
    """
    Verifica que la ventana de verificación se inicializa correctamente.

    Args:
        qtbot: Fixture de `pytest-qt` utilizada para controlar widgets Qt durante las pruebas.

    Asserts:
        - La ventana no debe ser `None`.
        - Debe tener un título no vacío.
    """
    ventana = iniciar_ventana_verificar()
    qtbot.addWidget(ventana)

    assert ventana is not None, "❌ No se pudo crear la ventana de verificación."
    assert ventana.windowTitle() != "", "❌ Falta título en la ventana de verificación."
