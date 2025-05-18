# pruebas/test_compraventa_consultas.py
# ──────────────────────────────────────
"""
Pruebas unitarias para el módulo `compraventa_consultas`.

Se utilizan mocks para interceptar llamadas a la base de datos,
asegurando que no se realicen operaciones reales durante los tests.

Las funciones verificadas incluyen:
- Obtención de vehículos disponibles.
- Inserción de nuevos vehículos.
- Recuperación del ID de cliente.
- Registro de ventas.
- Manejo de errores en transacciones.

Todas las pruebas simulan la conexión y el cursor mediante `unittest.mock`.
"""

import pytest
from unittest.mock import MagicMock, patch
import modelos.compraventa_consulta as consultas


@patch("modelos.compraventa_consulta.obtener_conexion")
def test_obtener_vehiculos_disponibles_retorna_lista(mock_conexion):
    """
    Verifica que `obtener_vehiculos_disponibles()` devuelve una lista
    con al menos un vehículo correctamente estructurado.
    """
    mock_cursor = MagicMock()
    mock_cursor.description = [
        ("id",), ("matricula",), ("marca",), ("modelo",),
        ("version",), ("anio",), ("bastidor",), ("color",),
        ("combustible",), ("kilometros",), ("potencia_cv",), ("cambio",),
        ("puertas",), ("plazas",), ("precio_compra",), ("precio_venta",),
        ("descuento_max",), ("estado",)
    ]
    mock_cursor.fetchall.return_value = [
        (1, "1234ABC", "Toyota", "Yaris", "Sport", 2020, "B123", "Rojo", "Gasolina",
         30000, 90, "Manual", 5, 5, 8000, 12000, 0, "DISPONIBLE")
    ]
    mock_con = MagicMock()
    mock_con.cursor.return_value = mock_cursor
    mock_conexion.return_value = mock_con

    resultado = consultas.obtener_vehiculos_disponibles()
    assert isinstance(resultado, list)
    assert len(resultado) == 1
    assert resultado[0]["matricula"] == "1234ABC"


@patch("modelos.compraventa_consulta.obtener_conexion")
def test_insertar_nuevo_vehiculo_ejecuta_insert(mock_conexion):
    """
    Verifica que `insertar_nuevo_vehiculo()` realiza la inserción y commit correctamente.
    """
    mock_cursor = MagicMock()
    mock_con = MagicMock()
    mock_con.cursor.return_value = mock_cursor
    mock_conexion.return_value = mock_con

    datos = {
        "marca": "Toyota", "modelo": "Yaris", "version": "Sport", "anio": 2023,
        "matricula": "TEST123", "bastidor": "XYZ789", "color": "Rojo", "combustible": "Gasolina",
        "kilometros": 50000, "potencia_cv": 90, "cambio": "Manual", "puertas": 5, "plazas": 5,
        "precio_compra": 8000, "precio_venta": 12000, "descuento_maximo": 0, "estado": "DISPONIBLE",
        "origen_compra": "Concesionario", "cliente_id": 1, "observaciones": "Ninguna",
        "descuento_max": 0, "dir_contrato": "/ruta/ficticia"
    }

    consultas.insertar_nuevo_vehiculo(datos)
    mock_cursor.execute.assert_called_once()
    mock_con.commit.assert_called_once()


@patch("modelos.compraventa_consulta.obtener_conexion")
def test_obtener_id_cliente_devuelve_id(mock_conexion):
    """
    Verifica que `obtener_id_cliente()` devuelve el ID correcto si el cliente existe.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (42,)
    mock_con = MagicMock()
    mock_con.cursor.return_value = mock_cursor
    mock_conexion.return_value = mock_con

    resultado = consultas.obtener_id_cliente("12345678A")
    assert resultado == 42


@patch("modelos.compraventa_consulta.obtener_conexion")
def test_obtener_id_cliente_no_encontrado(mock_conexion):
    """
    Verifica que `obtener_id_cliente()` devuelva None si el cliente no existe.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_con = MagicMock()
    mock_con.cursor.return_value = mock_cursor
    mock_conexion.return_value = mock_con

    resultado = consultas.obtener_id_cliente("00000000Z")
    assert resultado is None


@patch("modelos.compraventa_consulta.obtener_conexion")
def test_registrar_venta_insert_y_update(mock_conexion):
    """
    Verifica que `registrar_venta()` realiza dos operaciones (insert y update) 
    y hace commit correctamente.
    """
    mock_cursor = MagicMock()
    mock_con = MagicMock()
    mock_con.cursor.return_value = mock_cursor
    mock_conexion.return_value = mock_con

    consultas.registrar_venta(
        1, 2, 15000, "/ruta/factura.pdf", "/contrato/final")
    assert mock_cursor.execute.call_count == 2
    mock_con.commit.assert_called_once()


@patch("modelos.compraventa_consulta.obtener_conexion")
def test_registrar_venta_error_hace_rollback(mock_conexion):
    """
    Verifica que si ocurre una excepción en `registrar_venta()`,
    se realiza rollback sobre la transacción.
    """
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("Error en base de datos")
    mock_con = MagicMock()
    mock_con.cursor.return_value = mock_cursor
    mock_conexion.return_value = mock_con

    with pytest.raises(Exception, match="Error en base de datos"):
        consultas.registrar_venta(
            1, 2, 15000, "/ruta/factura.pdf", "/contrato/final")

    mock_con.rollback.assert_called_once()
