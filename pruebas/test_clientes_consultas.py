"""
Módulo de pruebas unitarias para las funciones del módulo `clientes_consultas.py`.

Estas pruebas validan el comportamiento de:
- Comprobación de existencia de DNI.
- Creación, eliminación y actualización de clientes.
- Consultas por nombre, ID y nombre completo.
- Operaciones que devuelven datos procesados desde la base de datos.

Todas las funciones que interactúan con PostgreSQL se simulan mediante mocks con `unittest.mock`.

Autor: Cresnik
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

import pytest
from unittest.mock import patch, MagicMock
from modelos import clientes_consultas


@patch("modelos.clientes_consultas.obtener_conexion")
def test_dni_ya_existe_true(mock_conexion):
    """Debe devolver True si el DNI ya existe en la base de datos."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_conexion.return_value.cursor.return_value = mock_cursor

    assert clientes_consultas.dni_ya_existe("12345678Z") is True


@patch("modelos.clientes_consultas.obtener_conexion")
def test_dni_ya_existe_false(mock_conexion):
    """Debe devolver False si el DNI no existe en la base de datos."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conexion.return_value.cursor.return_value = mock_cursor

    assert clientes_consultas.dni_ya_existe("00000000X") is False


@patch("modelos.clientes_consultas.obtener_conexion")
def test_crear_cliente_exito(mock_conexion):
    """Debe devolver True si la creación del cliente fue exitosa."""
    mock_conexion.return_value.cursor.return_value = MagicMock()
    assert clientes_consultas.crear_cliente(
        "Luis", "Perez", "", "12345678Z", "", "", "", "", "", "", "")


@patch("modelos.clientes_consultas.obtener_conexion")
def test_crear_cliente_fallo(mock_conexion):
    """Debe devolver False si hay una excepción durante la creación del cliente."""
    mock_conexion.side_effect = Exception("Error de conexión")
    assert clientes_consultas.crear_cliente(
        "Luis", "Perez", "", "12345678Z", "", "", "", "", "", "", "") is False


@patch("modelos.clientes_consultas.obtener_conexion")
def test_obtener_nombres_completos(mock_conexion):
    """Debe devolver una lista de nombres completos correctamente formateados."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("Luis Perez",), ("Ana Lopez",)]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = clientes_consultas.obtener_nombres_completos()
    assert resultado == ["Luis Perez", "Ana Lopez"]


@patch("modelos.clientes_consultas.obtener_conexion")
def test_obtener_datos_cliente_por_nombre(mock_conexion):
    """Debe devolver los datos completos del cliente según nombre completo."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, 2, 3)
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = clientes_consultas.obtener_datos_cliente_por_nombre(
        "Luis Perez")
    assert resultado == (1, 2, 3)


@patch("modelos.clientes_consultas.obtener_conexion")
def test_buscar_clientes_por_nombre(mock_conexion):
    """Debe devolver lista de tuplas con nombres completos e IDs."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, "Luis", "Perez", ""), (2, "Ana", "Lopez", "Martinez")]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = clientes_consultas.buscar_clientes_por_nombre()
    assert resultado == [("Luis Perez", 1), ("Ana Lopez Martinez", 2)]


@patch("modelos.clientes_consultas.obtener_conexion")
def test_obtener_cliente_por_id(mock_conexion):
    """Debe devolver un diccionario con los datos del cliente según su ID."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [
        "Luis", "Perez", "", "12345678Z", "", "", "", "", "", "", ""]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = clientes_consultas.obtener_cliente_por_id(1)
    assert resultado["nombre"] == "Luis"


@patch("modelos.clientes_consultas.obtener_conexion")
def test_obtener_clientes(mock_conexion):
    """Debe devolver una lista de diccionarios representando los clientes."""
    mock_cursor = MagicMock()
    mock_cursor.description = [("id",), ("nombre",)]
    mock_cursor.fetchall.return_value = [(1, "Luis")]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = clientes_consultas.obtener_clientes()
    assert resultado == [{"id": 1, "nombre": "Luis"}]


@patch("modelos.clientes_consultas.obtener_conexion")
def test_actualizar_cliente_exito(mock_conexion):
    """Debe devolver True si se actualiza correctamente un cliente."""
    mock_conexion.return_value.cursor.return_value = MagicMock()
    resultado = clientes_consultas.actualizar_cliente(
        1, "Luis", "Perez", "", "12345678Z", "", "", "", "", "", "", "")
    assert resultado is True


@patch("modelos.clientes_consultas.obtener_conexion")
def test_actualizar_cliente_fallo(mock_conexion):
    """Debe devolver False si ocurre un error durante la actualización."""
    mock_conexion.side_effect = Exception("Error")
    resultado = clientes_consultas.actualizar_cliente(
        1, "Luis", "Perez", "", "12345678Z", "", "", "", "", "", "", "")
    assert resultado is False


@patch("modelos.clientes_consultas.obtener_conexion")
def test_eliminar_cliente_por_id_exito(mock_conexion):
    """Debe devolver True si el cliente se elimina correctamente."""
    mock_conexion.return_value.cursor.return_value = MagicMock()
    resultado = clientes_consultas.eliminar_cliente_por_id(1)
    assert resultado is True


@patch("modelos.clientes_consultas.obtener_conexion")
def test_eliminar_cliente_por_id_fallo(mock_conexion):
    """Debe devolver False si hay un error al eliminar al cliente."""
    mock_conexion.side_effect = Exception("Error")
    resultado = clientes_consultas.eliminar_cliente_por_id(1)
    assert resultado is False


@patch("modelos.clientes_consultas.obtener_conexion")
def test_crear_cliente_y_devolver_id(mock_conexion):
    """Debe devolver el ID del nuevo cliente si la operación es exitosa."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [99]
    mock_conexion.return_value.cursor.return_value = mock_cursor

    resultado = clientes_consultas.crear_cliente_y_devolver_id(
        "Luis", "Perez", "", "12345678Z", "", "", "", "", "", "", "")
    assert resultado == 99


@patch("modelos.clientes_consultas.obtener_conexion")
def test_crear_cliente_y_devolver_id_fallo(mock_conexion):
    """Debe devolver None si hay una excepción durante la creación."""
    mock_conexion.side_effect = Exception("Error")
    resultado = clientes_consultas.crear_cliente_y_devolver_id(
        "Luis", "Perez", "", "12345678Z", "", "", "", "", "", "", "")
    assert resultado is None
