"""
Pruebas unitarias del módulo `recepcionamiento_consultas`.

Este conjunto de tests verifica que las funciones encargadas de obtener datos
para la funcionalidad de recepcionamiento devuelven resultados esperados
y manejan correctamente los datos provenientes de la base de datos simulada.

Se utiliza `pytest` junto con `unittest.mock` para evitar accesos reales
a la base de datos, simulando respuestas con datos de ejemplo.
"""

import pytest
from unittest.mock import patch, MagicMock
import modelos.recepcionamiento_consultas as consultas


@pytest.fixture
def mock_conexion():
    """
    Simula la conexión a la base de datos reemplazando `obtener_conexion`
    por un mock, que se puede usar en todos los tests que acceden a la BD.
    """
    with patch("modelos.recepcionamiento_consultas.obtener_conexion") as mock:
        yield mock


def test_obtener_clientes_retorna_lista(mock_conexion):
    """
    Verifica que `obtener_clientes` devuelve una lista de diccionarios con
    información del cliente (nombre, apellidos, dni, etc.).
    """
    cursor_mock = MagicMock()
    cursor_mock.description = [
        ("nombre",), ("primer_apellido",), ("segundo_apellido",), ("dni",),
        ("telefono",), ("email",), ("direccion",)
    ]
    cursor_mock.fetchall.return_value = [
        ("Juan", "Pérez", "Gómez", "12345678Z",
         "123456789", "juan@correo.com", "Calle Falsa 123")
    ]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_clientes()
    assert isinstance(resultado, list)
    assert resultado[0]["nombre"] == "Juan"


def test_obtener_matriculas_existentes_retorna_lista(mock_conexion):
    """
    Verifica que `obtener_matriculas_existentes` devuelve una lista simple de matrículas.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("1234ABC",), ("5678XYZ",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_matriculas_existentes()
    assert resultado == ["1234ABC", "5678XYZ"]


def test_obtener_datos_vehiculo_por_matricula_ok(mock_conexion):
    """
    Verifica que `obtener_datos_vehiculo_por_matricula` devuelve los datos correctos
    para una matrícula existente (marca, modelo, tipo, etc.).
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (
        "Toyota", "Corolla", "Rojo", 2020, "Gasolina", "VIN123456",
        "Turismo", "Sedán"
    )
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_datos_vehiculo_por_matricula("1234ABC")
    assert resultado["marca"] == "Toyota"
    assert resultado["tipo"] == "Sedán"


def test_obtener_categorias_vehiculo(mock_conexion):
    """
    Verifica que `obtener_categorias_vehiculo` devuelve una lista con categorías válidas.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("Turismo",), ("Camión",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_categorias_vehiculo()
    assert resultado == ["Turismo", "Camión"]


def test_obtener_combustibles(mock_conexion):
    """
    Comprueba que `obtener_combustibles` devuelve una lista de tipos de combustible.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("Gasolina",), ("Diésel",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_combustibles()
    assert resultado == ["Gasolina", "Diésel"]


def test_obtener_motivos(mock_conexion):
    """
    Verifica que `obtener_motivos` devuelve una lista de motivos de intervención.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [(1, "Revisión"), (2, "Avería")]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_motivos()
    assert resultado[0]["nombre"] == "Revisión"


def test_obtener_urgencias(mock_conexion):
    """
    Comprueba que `obtener_urgencias` devuelve una lista de niveles de urgencia.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [(1, "Alta"), (2, "Media")]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_urgencias()
    assert resultado[1]["descripcion"] == "Media"


def test_obtener_matriculas(mock_conexion):
    """
    Verifica que `obtener_matriculas` devuelve una lista de matrículas registradas.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("1234ABC",), ("5678XYZ",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_matriculas()
    assert resultado == ["1234ABC", "5678XYZ"]


def test_obtener_tipos_vehiculo(mock_conexion):
    """
    Comprueba que `obtener_tipos_vehiculo` devuelve tipos y categorías correctamente estructurados.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [
        ("Turismo", "Sedán"), ("Camión", "Pickup")]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_tipos_vehiculo()
    assert resultado[0]["categoria"] == "Turismo"
    assert resultado[1]["nombre"] == "Pickup"


def test_obtener_matriculas_por_cliente(mock_conexion):
    """
    Verifica que `obtener_matriculas_por_cliente` devuelve todas las matrículas
    asociadas a un DNI específico.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("1234ABC",), ("9999ZZZ",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_matriculas_por_cliente("12345678Z")
    assert resultado == ["1234ABC", "9999ZZZ"]


def test_obtener_siguiente_numero_recepcionamiento(mock_conexion):
    """
    Comprueba que `obtener_siguiente_numero_recepcionamiento` incrementa el número correctamente.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (15,)
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_siguiente_numero_recepcionamiento()
    assert resultado == 16


def test_obtener_cliente_id_por_dni(mock_conexion):
    """
    Verifica que `obtener_cliente_id_por_dni` devuelve correctamente el ID del cliente.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (42,)
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_cliente_id_por_dni("12345678Z")
    assert resultado == 42


def test_obtener_vehiculo_id_por_matricula(mock_conexion):
    """
    Comprueba que `obtener_vehiculo_id_por_matricula` devuelve el ID del vehículo correctamente.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (99,)
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_vehiculo_id_por_matricula("1234ABC")
    assert resultado == 99


def test_obtener_estado_id_por_defecto(mock_conexion):
    """
    Verifica que `obtener_estado_id_por_defecto` devuelve el ID del estado por defecto configurado.
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (5,)
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_estado_id_por_defecto()
    assert resultado == 5


def test_obtener_datos_completos_recepcionamiento(mock_conexion):
    """
    Comprueba que `obtener_datos_completos_recepcionamiento` agrupa correctamente
    toda la información relevante (motivos, urgencias, categorías, tipos y combustibles).
    """
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [
        ("motivo", 1, "Revisión"),
        ("urgencia", 2, "Alta"),
        ("categoria", None, "Turismo"),
        ("tipo", None, "SUV"),
        ("combustible", None, "Gasolina")
    ]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_datos_completos_recepcionamiento()
    assert resultado["motivos"][0]["nombre"] == "Revisión"
    assert resultado["urgencias"][0]["descripcion"] == "Alta"
    assert "Turismo" in resultado["categorias"]
    assert resultado["tipos"][0]["nombre"] == "SUV"
    assert "Gasolina" in resultado["combustibles"]
