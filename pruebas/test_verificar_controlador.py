"""
TEST UNITARIO: Controlador de verificación de código OTP.

Este test no prueba la lógica de verificación, pero asegura que la ventana se
construye correctamente y tiene los elementos esperados.
"""

import pytest
from pruebas.verificar_test import iniciar_ventana_verificar


def test_controlador_verificacion_crea_ventana(qtbot):
    """
    Verifica que la ventana de verificación se crea correctamente.
    """
    ventana = iniciar_ventana_verificar()
    qtbot.addWidget(ventana)

    assert ventana is not None
    assert ventana.windowTitle() != "", "Falta título en la ventana de verificación."
