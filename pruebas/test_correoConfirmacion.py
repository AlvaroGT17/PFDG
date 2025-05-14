import pytest
from pruebas.correoConfirmacion_test import iniciar_ventana_correo_confirmacion


def test_correo_confirmacion_instancia(qtbot):
    """
    Verifica que la ventana de confirmación de correo se crea correctamente.
    """
    ventana = iniciar_ventana_correo_confirmacion()
    qtbot.addWidget(ventana)

    assert ventana is not None
    assert ventana.windowTitle() != ""
    assert hasattr(ventana, "correo_seleccionado")
