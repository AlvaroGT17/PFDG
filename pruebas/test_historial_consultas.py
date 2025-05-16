# pruebas/test_historial_consultas.py
# ────────────────────────────────────
"""
Pruebas unitarias para las funciones del módulo `historial_consultas.py`.

Se valida el correcto funcionamiento de:
- obtención de fichajes personales.
- obtención de fichajes globales (admin).
- obtención del nombre del usuario a partir de su ID.

Todas las funciones que interactúan con la base de datos se simulan mediante mocks.
"""

import pytest
from unittest.mock import patch, MagicMock
import modelos.historial_consultas as consultas


@patch("modelos.historial_consultas.obtener_conexion")
def test_obtener_fichajes_personales(mock_conexion):
    """Debe devolver una lista con los fichajes del usuario."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("2025-05-01 08:00:00", "ENTRADA"),
        ("2025-05-01 17:00:00", "SALIDA")
    ]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = consultas.obtener_fichajes_personales(usuario_id=1)

    assert isinstance(resultado, list)
    assert resultado[0][1] == "ENTRADA"
    assert resultado[1][1] == "SALIDA"


@patch("modelos.historial_consultas.obtener_conexion")
def test_obtener_fichajes_globales(mock_conexion):
    """Debe devolver una lista con todos los fichajes y nombres de usuario."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("2025-05-01 08:00:00", "ENTRADA", "CRESNIK"),
        ("2025-05-01 17:00:00", "SALIDA", "CRESNIK")
    ]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = consultas.obtener_fichajes_globales()

    assert isinstance(resultado, list)
    assert resultado[0][2] == "CRESNIK"


@patch("modelos.historial_consultas.obtener_conexion")
def test_obtener_nombre_usuario_existe(mock_conexion):
    """Debe devolver el nombre del usuario si existe en la base de datos."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ["CRESNIK"]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    nombre = consultas.obtener_nombre_usuario(usuario_id=1)
    assert nombre == "CRESNIK"


@patch("modelos.historial_consultas.obtener_conexion")
def test_obtener_nombre_usuario_no_existe(mock_conexion):
    """Debe devolver 'Desconocido' si el usuario no existe."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conexion.return_value.cursor.return_value = mock_cursor

    nombre = consultas.obtener_nombre_usuario(usuario_id=999)
    assert nombre == "Desconocido"
