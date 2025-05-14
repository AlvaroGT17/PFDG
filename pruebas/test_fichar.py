import pytest
from pruebas.fichar_test import iniciar_ventana_fichar


def test_fichar_se_instancia_correctamente(qtbot):
    """
    Verifica que el controlador de fichaje se instancia correctamente
    y contiene una ventana.
    """
    controlador = iniciar_ventana_fichar()
    qtbot.addWidget(controlador.ventana)

    assert controlador is not None
    assert hasattr(controlador, "ventana")
