# pruebas/test_historial_consultas.py
# ────────────────────────────────────
"""
Pruebas unitarias para las funciones del módulo `historial_consultas.py`.

Se valida el correcto funcionamiento de:
- La obtención de fichajes personales.
- La obtención de fichajes globales (modo administrador).
- La obtención del nombre del usuario a partir de su ID.

Todas las funciones que interactúan con la base de datos se simulan
mediante mocks para evitar dependencias externas.

Se asegura que los resultados devueltos por las funciones tengan la estructura
y contenido esperados bajo distintos escenarios.
"""

import pytest
from unittest.mock import patch, MagicMock
import modelos.historial_consultas as consultas


@patch("modelos.historial_consultas.obtener_conexion")
def test_obtener_fichajes_personales(mock_conexion):
    """
    Verifica que `obtener_fichajes_personales` devuelve una lista de fichajes
    con tipo (ENTRADA/SALIDA) correctamente formateados.
    """
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
    """
    Verifica que `obtener_fichajes_globales` devuelve una lista de fichajes
    con los nombres de los usuarios incluidos en cada registro.
    """
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
    """
    Verifica que `obtener_nombre_usuario` devuelve el nombre correcto
    cuando el usuario existe en la base de datos.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ["CRESNIK"]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    nombre = consultas.obtener_nombre_usuario(usuario_id=1)
    assert nombre == "CRESNIK"


@patch("modelos.historial_consultas.obtener_conexion")
def test_obtener_nombre_usuario_no_existe(mock_conexion):
    """
    Verifica que `obtener_nombre_usuario` devuelve 'Desconocido' si no se encuentra
    ningún registro asociado al ID de usuario proporcionado.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conexion.return_value.cursor.return_value = mock_cursor

    nombre = consultas.obtener_nombre_usuario(usuario_id=999)
    assert nombre == "Desconocido"
