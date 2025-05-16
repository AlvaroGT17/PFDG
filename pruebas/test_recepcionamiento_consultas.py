import pytest
from unittest.mock import patch, MagicMock
import modelos.recepcionamiento_consultas as consultas


@pytest.fixture
def mock_conexion():
    with patch("modelos.recepcionamiento_consultas.obtener_conexion") as mock:
        yield mock


def test_obtener_clientes_retorna_lista(mock_conexion):
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
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("1234ABC",), ("5678XYZ",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_matriculas_existentes()
    assert resultado == ["1234ABC", "5678XYZ"]


def test_obtener_datos_vehiculo_por_matricula_ok(mock_conexion):
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
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("Turismo",), ("Camión",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_categorias_vehiculo()
    assert resultado == ["Turismo", "Camión"]


def test_obtener_combustibles(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("Gasolina",), ("Diésel",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_combustibles()
    assert resultado == ["Gasolina", "Diésel"]


def test_obtener_motivos(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [(1, "Revisión"), (2, "Avería")]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_motivos()
    assert resultado[0]["nombre"] == "Revisión"


def test_obtener_urgencias(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [(1, "Alta"), (2, "Media")]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_urgencias()
    assert resultado[1]["descripcion"] == "Media"


@pytest.fixture
def mock_conexion():
    with patch("modelos.recepcionamiento_consultas.obtener_conexion") as mock:
        yield mock


def test_obtener_matriculas(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("1234ABC",), ("5678XYZ",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_matriculas()
    assert resultado == ["1234ABC", "5678XYZ"]


def test_obtener_tipos_vehiculo(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [
        ("Turismo", "Sedán"), ("Camión", "Pickup")]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_tipos_vehiculo()
    assert resultado[0]["categoria"] == "Turismo"
    assert resultado[1]["nombre"] == "Pickup"


def test_obtener_matriculas_por_cliente(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [("1234ABC",), ("9999ZZZ",)]
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_matriculas_por_cliente("12345678Z")
    assert resultado == ["1234ABC", "9999ZZZ"]


def test_obtener_siguiente_numero_recepcionamiento(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (15,)
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_siguiente_numero_recepcionamiento()
    assert resultado == 16


def test_obtener_cliente_id_por_dni(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (42,)
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_cliente_id_por_dni("12345678Z")
    assert resultado == 42


def test_obtener_vehiculo_id_por_matricula(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (99,)
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_vehiculo_id_por_matricula("1234ABC")
    assert resultado == 99


def test_obtener_estado_id_por_defecto(mock_conexion):
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (5,)
    mock_conexion.return_value.cursor.return_value = cursor_mock

    resultado = consultas.obtener_estado_id_por_defecto()
    assert resultado == 5


def test_obtener_datos_completos_recepcionamiento(mock_conexion):
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
