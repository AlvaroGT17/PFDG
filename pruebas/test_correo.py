import pytest
from unittest.mock import patch
from pruebas import correo_test


@patch("pruebas.correo_test.enviar_correo")
def test_envio_correo(mock_enviar):
    """
    Verifica que se llama a la función enviar_correo con los parámetros esperados.
    """
    correo_test.probar_envio_correo()
    mock_enviar.assert_called_once_with(
        "cresnik17021983@gmail.com", "CRESNIK", "123456")
