"""
Pruebas unitarias para `enviar_correo_presupuesto`.

Se verifican dos escenarios principales:
- Envío exitoso del correo con un PDF adjunto.
- Manejo correcto de un error durante el envío.

Las dependencias como `os.getenv`, `open` y `smtplib.SMTP_SSL` son simuladas con `unittest.mock`.
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
from utilidades.correo_presupuesto import enviar_correo_presupuesto


@patch("utilidades.correo_presupuesto.smtplib.SMTP_SSL")
@patch("utilidades.correo_presupuesto.open", new_callable=mock_open, read_data=b"%PDF-dummy-content")
@patch("utilidades.correo_presupuesto.os.getenv")
def test_enviar_correo_presupuesto_exitoso(mock_getenv, mock_open_file, mock_smtp):
    """
    Verifica que el envío de correo se realiza correctamente si no hay errores.
    """
    # Simular variables de entorno
    mock_getenv.side_effect = lambda key: {
        "EMAIL_USER": "reyboxes@test.com",
        "EMAIL_PASS": "secreta"
    }[key]

    # Simular conexión SMTP
    mock_servidor = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_servidor

    resultado, error = enviar_correo_presupuesto(
        "cliente@correo.com", "ruta/ficticia.pdf", {"cliente": "cresnik"}
    )

    assert resultado is True
    assert error is None
    mock_servidor.send_message.assert_called_once()


@patch("utilidades.correo_presupuesto.smtplib.SMTP_SSL", side_effect=Exception("Error de conexión"))
@patch("utilidades.correo_presupuesto.open", new_callable=mock_open, read_data=b"%PDF-dummy-content")
@patch("utilidades.correo_presupuesto.os.getenv")
def test_enviar_correo_presupuesto_falla(mock_getenv, mock_open_file, mock_smtp):
    """
    Verifica que se maneja correctamente un fallo en la conexión SMTP.
    """
    # Simular variables de entorno
    mock_getenv.side_effect = lambda key: {
        "EMAIL_USER": "reyboxes@test.com",
        "EMAIL_PASS": "secreta"
    }[key]

    resultado, error = enviar_correo_presupuesto(
        "cliente@correo.com", "ruta/ficticia.pdf", {"cliente": "cresnik"}
    )

    assert resultado is False
    assert isinstance(error, str)
