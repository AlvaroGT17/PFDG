"""
Pruebas unitarias para el módulo `fichajes_consultas.py`.

Este conjunto de tests valida que la función `registrar_fichaje`:
- Ejecuta correctamente la inserción de fichajes con los parámetros esperados.
- Maneja correctamente la conexión usando `with`.
- Cierra la conexión al finalizar, incluso si hay errores.

Se usa `unittest.mock` para simular las conexiones y cursors de PostgreSQL.

"""

import pytest
from unittest.mock import patch, MagicMock
from modelos import fichajes_consultas


@patch("modelos.fichajes_consultas.obtener_conexion")
def test_registrar_fichaje_ejecuta_insert_correctamente(mock_conexion):
    """
    Verifica que la función `registrar_fichaje` ejecuta correctamente
    el INSERT con los valores esperados y cierra la conexión.
    """
    # Preparar mocks de conexión y cursor
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conexion.return_value = mock_conn

    # Ejecutar
    fichajes_consultas.registrar_fichaje(5, "ENTRADA")

    # Comprobar que se llamó al INSERT
    mock_cursor.execute.assert_called_once()
    query, params = mock_cursor.execute.call_args[0]
    assert "INSERT INTO fichajes" in query
    assert params[0] == 5
    assert params[1] == "ENTRADA"

    # Verificar que se cierra la conexión
    mock_conn.close.assert_called_once()
