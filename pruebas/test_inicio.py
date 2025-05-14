import pytest
from unittest.mock import patch
from vistas.ventana_inicio import VentanaInicio


def test_inicio_se_inicializa_correctamente(qtbot):
    """
    Verifica que se puede instanciar la ventana sin ejecutar su lógica interna (para evitar errores).
    """
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Cresnik", "ADMINISTRADOR")
        qtbot.addWidget(ventana)
        assert ventana.nombre == "CRESNIK"
        assert ventana.rol == "ADMINISTRADOR"


def test_inicio_tiene_botones(qtbot):
    """
    Verifica que los atributos principales existen incluso si no se inicializa la interfaz completa.
    """
    with patch.object(VentanaInicio, "inicializar_ui", return_value=None):
        ventana = VentanaInicio("Cresnik", "ADMINISTRADOR")
        qtbot.addWidget(ventana)
        assert hasattr(ventana, "botones")
