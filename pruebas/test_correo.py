"""
Pruebas unitarias para la función `enviar_correo` del módulo `utilidades.correo`.

Se prueban dos escenarios clave:
- Envío exitoso de correo con HTML generado correctamente.
- Manejo adecuado de errores durante el envío por SMTP.

Todas las llamadas a red, lectura de variables de entorno y uso de SMTP son
simuladas mediante mocks para evitar efectos secundarios reales.

"""

import pytest
from unittest.mock import patch, MagicMock
from utilidades.correo import enviar_correo


@patch("utilidades.correo.smtplib.SMTP_SSL")
@patch("utilidades.correo.os.getenv")
def test_envio_correo_exitoso(mock_getenv, mock_smtp):
    """
    Verifica que se envía un correo correctamente con la plantilla HTML,
    y que contiene el código y el nombre del usuario capitalizado.

    También comprueba que no se incluya el nombre original sin capitalizar.
    """
    # Simular credenciales del entorno
    mock_getenv.side_effect = lambda key: {
        "EMAIL_USER": "reyboxes@test.com",
        "EMAIL_PASS": "secreta"
    }[key]

    # Simular conexión SMTP
    mock_servidor = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_servidor

    # Ejecutar función
    enviar_correo("cliente@correo.com", "cresnik", "ABC123")

    # Validaciones
    mock_servidor.login.assert_called_once_with("reyboxes@test.com", "secreta")
    mock_servidor.send_message.assert_called_once()

    mensaje_enviado = mock_servidor.send_message.call_args[0][0]

    # Extraer parte HTML del mensaje
    for parte in mensaje_enviado.get_payload():
        if parte.get_content_type() == "text/html":
            html = parte.get_payload(decode=True).decode("utf-8")
            break
    else:
        raise AssertionError("No se encontró la parte HTML en el mensaje")

    # Verificaciones del contenido
    assert "ABC123" in html                  # Código incluido
    assert "cresnik" not in html             # Nombre sin capitalizar no debe aparecer
    assert "Cresnik" in html                 # Nombre correctamente capitalizado


@patch("utilidades.correo.smtplib.SMTP_SSL")
@patch("utilidades.correo.os.getenv")
def test_envio_correo_falla_con_excepcion(mock_getenv, mock_smtp):
    """
    Simula una excepción durante la conexión SMTP y verifica que se propaga correctamente.
    """
    # Simular credenciales
    mock_getenv.side_effect = lambda key: {
        "EMAIL_USER": "reyboxes@test.com",
        "EMAIL_PASS": "secreta"
    }[key]

    # Simular fallo en la conexión
    mock_smtp.side_effect = Exception("Fallo de red")

    # Ejecutar y verificar que lanza excepción
    with pytest.raises(Exception, match="Fallo de red"):
        enviar_correo("cliente@correo.com", "cresnik", "XYZ789")
