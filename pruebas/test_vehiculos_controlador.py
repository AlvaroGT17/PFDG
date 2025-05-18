"""
TEST UNITARIOS: Controlador de gestión de vehículos (`vehiculos_controlador.py`)

Este módulo contiene pruebas automatizadas para verificar que:
1. El controlador de vehículos inicializa correctamente todos los datos necesarios.
2. El sistema de autocompletado y los combos se configuran correctamente.
3. La búsqueda por matrícula dispara la función esperada.

Dependencias:
- pytest
- pytest-qt
- unittest.mock
- PySide6

Se mockean todas las llamadas a la base de datos y lógica interna para simular
el entorno gráfico sin depender de datos reales.
"""

import pytest
from unittest.mock import patch, MagicMock
from controladores.vehiculos_controlador import VehiculosControlador
from PySide6.QtWidgets import QCompleter


@patch("controladores.vehiculos_controlador.obtener_clientes")
@patch("controladores.vehiculos_controlador.obtener_combustibles")
@patch("controladores.vehiculos_controlador.obtener_matriculas_existentes")
@patch("controladores.vehiculos_controlador.obtener_categorias")
def test_vehiculos_controlador_inicializa_correctamente(
    mock_obtener_categorias,
    mock_obtener_matriculas,
    mock_obtener_combustibles,
    mock_obtener_clientes,
    qtbot,
):
    """
    Verifica que el controlador `VehiculosControlador` inicializa correctamente
    los combos y campos de búsqueda con valores simulados.

    Mocks:
        - obtener_clientes()
        - obtener_combustibles()
        - obtener_matriculas_existentes()
        - obtener_categorias()

    Asserts:
        - Los combos de categoría y combustible tienen al menos un valor cargado.
        - Los campos de búsqueda usan QCompleter correctamente.
        - Los botones de modificar y eliminar están deshabilitados al iniciar.
    """
    mock_obtener_clientes.return_value = [
        {"id": 1, "nombre": "Juan", "primer_apellido": "Pérez",
         "segundo_apellido": "López", "dni": "12345678A"},
    ]
    mock_obtener_combustibles.return_value = [{"id": 1, "nombre": "Gasolina"}]
    mock_obtener_matriculas.return_value = ["1234ABC", "5678DEF"]
    mock_obtener_categorias.return_value = ["Turismo", "Furgoneta"]

    controlador = VehiculosControlador(ventana_anterior=MagicMock())
    qtbot.addWidget(controlador.ventana)

    assert controlador.ventana.combo_categoria.count() > 1, "❌ Combo categoría vacío"
    assert controlador.ventana.combo_combustible.count() > 1, "❌ Combo combustible vacío"

    assert isinstance(
        controlador.ventana.input_buscar_nombre.completer(), QCompleter)
    assert isinstance(
        controlador.ventana.input_buscar_dni.completer(), QCompleter)
    assert isinstance(
        controlador.ventana.input_buscar_matricula.completer(), QCompleter)

    assert not controlador.ventana.boton_modificar.isEnabled(
    ), "❌ Botón Modificar debería estar deshabilitado"
    assert not controlador.ventana.boton_eliminar.isEnabled(
    ), "❌ Botón Eliminar debería estar deshabilitado"


@patch("controladores.vehiculos_controlador.buscar_vehiculo_por_matricula")
@patch("controladores.vehiculos_controlador.obtener_clientes", return_value=[])
@patch("controladores.vehiculos_controlador.obtener_combustibles", return_value=[])
@patch("controladores.vehiculos_controlador.obtener_matriculas_existentes", return_value=[])
@patch("controladores.vehiculos_controlador.obtener_categorias", return_value=[])
def test_busqueda_matricula_dispara_funcion_correcta(
    mock_cat, mock_mat, mock_comb, mock_cli, mock_buscar, qtbot
):
    """
    Verifica que al ingresar una matrícula en el campo correspondiente y ejecutar
    la función `buscar_vehiculo_desde_input()`, se llama correctamente a la función
    `buscar_vehiculo()` con la matrícula introducida.

    Asserts:
        - `buscar_vehiculo()` se llama exactamente una vez con la matrícula esperada.
    """
    controlador = VehiculosControlador(ventana_anterior=MagicMock())
    qtbot.addWidget(controlador.ventana)

    controlador.ventana.input_buscar_matricula.setText("9999XYZ")
    controlador.buscar_vehiculo = MagicMock()
    controlador.buscar_vehiculo_desde_input()

    controlador.buscar_vehiculo.assert_called_once_with("9999XYZ")
