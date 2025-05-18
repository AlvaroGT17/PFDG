# pruebas/test_presupuesto_consultas.py
"""
Tests unitarios para el módulo `presupuesto_consultas`.

Este conjunto de pruebas valida las funciones relacionadas con el tratamiento
de presupuestos dentro de la base de datos, incluyendo:

- La obtención de recepcionamientos disponibles para presupuestar.
- La inserción de presupuestos y la recuperación de su ID.
- La inserción de tareas asociadas a presupuestos.

Se utilizan mocks para evitar el uso de una base de datos real durante las pruebas.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

import pytest
from unittest.mock import patch, MagicMock
import modelos.presupuesto_consultas as consultas


@pytest.fixture
def mock_conexion():
    """
    Simula una conexión y cursor de base de datos.

    Devuelve una tupla `(conn, cursor)` con métodos mockeados.
    Verifica además que `conn.close()` se llama al finalizar.
    """
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    yield mock_conn, mock_cursor
    mock_conn.close.assert_called_once()


def test_obtener_recepciones_para_presupuesto(mock_conexion):
    """
    Verifica que la función `obtener_recepciones_para_presupuesto` retorna 
    correctamente una lista de recepciones disponibles con los campos esperados.
    """
    conn, cursor = mock_conexion

    # Simular columnas y datos
    cursor.description = [
        ("id",), ("num_recepcionamiento",), ("fecha",), ("precio_max_autorizado",),
        ("observaciones",), ("cliente",), ("correo_cliente",), ("matricula",)
    ]
    cursor.fetchall.return_value = [
        (1, "R-001", "2025-05-01 10:00", 500.0, "Sin novedades",
         "CRESNIK", "cresnik@email.com", "1234ABC")
    ]

    with patch("modelos.presupuesto_consultas.obtener_conexion", return_value=conn):
        resultado = consultas.obtener_recepciones_para_presupuesto()

    assert isinstance(resultado, list)
    assert resultado[0]["cliente"] == "CRESNIK"
    assert resultado[0]["matricula"] == "1234ABC"
    conn.close.assert_called_once()


def test_insertar_presupuesto_retorna_id(mock_conexion):
    """
    Verifica que `insertar_presupuesto` inserta correctamente los datos
    y devuelve el ID del nuevo presupuesto (simulado como 42).
    """
    conn, cursor = mock_conexion
    cursor.fetchone.return_value = [42]

    with patch("modelos.presupuesto_consultas.obtener_conexion", return_value=conn):
        presupuesto_id = consultas.insertar_presupuesto(
            recepcion_id=1,
            total=450.0,
            respuesta="Aceptado",
            ruta_pdf="documentos/presupuesto.pdf"
        )

    assert presupuesto_id == 42
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


def test_insertar_tarea_presupuesto_insert_correcto(mock_conexion):
    """
    Comprueba que `insertar_tarea_presupuesto` ejecuta correctamente 
    la inserción de una tarea asociada a un presupuesto.
    """
    conn, cursor = mock_conexion

    with patch("modelos.presupuesto_consultas.obtener_conexion", return_value=conn):
        consultas.insertar_tarea_presupuesto(
            presupuesto_id=42,
            descripcion="Cambio de aceite",
            horas=1.5,
            precio_hora=40.0,
            total=60.0
        )

    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()
    conn.close.assert_called_once()
