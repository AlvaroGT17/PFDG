"""
TESTS AUTOMÁTICOS: Ventana de gestión de vehículos (`VentanaVehiculos`)

Este módulo contiene pruebas automáticas enfocadas en validar:
1. Que la ventana se inicializa correctamente sin errores.
2. Que existen campos de búsqueda esenciales y correctamente etiquetados.
3. Que los botones principales de acción están presentes.

Requisitos:
- pytest
- pytest-qt
- PySide6

Las pruebas están diseñadas para asegurar la estabilidad visual
y funcional básica de la interfaz gráfica.

Estas validaciones se integran dentro del entorno de pruebas del sistema ReyBoxes.
"""

import pytest
from pruebas.vehiculos_test import iniciar_ventana_vehiculos
from PySide6.QtWidgets import QLineEdit


def test_ventana_vehiculos_se_inicializa(qtbot):
    """
    Verifica que la ventana `VentanaVehiculos` se crea sin errores.

    Usa `qtbot` para registrar la ventana en el entorno de prueba
    y confirma que su título no está vacío.

    Args:
        qtbot: Fixture proporcionada por `pytest-qt`.

    Asserts:
        - La ventana debe tener un título asignado.
    """
    ventana = iniciar_ventana_vehiculos()
    qtbot.addWidget(ventana)

    assert ventana.windowTitle() != "", "❌ La ventana no tiene título asignado."


def test_hay_campos_de_busqueda(qtbot):
    """
    Verifica que existen al menos dos campos de búsqueda funcionales (`QLineEdit`),
    y que al menos uno de ellos se refiere a "nombre" o "cliente".

    Esta prueba se adapta a interfaces modernas que utilizan `placeholderText`
    en lugar de `QLabel` visibles.

    Args:
        qtbot: Fixture de `pytest-qt`.

    Asserts:
        - Al menos 2 campos `QLineEdit` deben estar presentes.
        - Uno de ellos debe contener "nombre" o "cliente" como placeholder.
    """
    ventana = iniciar_ventana_vehiculos()
    qtbot.addWidget(ventana)

    campos = ventana.findChildren(QLineEdit)
    assert len(campos) >= 2, "❌ Faltan campos de entrada"

    placeholders = [c.placeholderText().lower()
                    for c in campos if c.placeholderText()]
    assert any(
        "nombre" in p or "cliente" in p for p in placeholders
    ), "❌ No hay campos con placeholder que contenga 'nombre' o 'cliente'"


def test_botones_de_accion_estan_presentes(qtbot):
    """
    Verifica que los botones principales de acción estén correctamente creados:
    - Registrar
    - Modificar
    - Limpiar
    - Eliminar
    - Volver

    Args:
        qtbot: Fixture de `pytest-qt`.

    Asserts:
        - Cada uno de los textos esperados debe estar presente entre los botones de acción.
    """
    ventana = iniciar_ventana_vehiculos()
    qtbot.addWidget(ventana)

    nombres_botones = [
        ventana.boton_guardar.text().lower(),
        ventana.boton_modificar.text().lower(),
        ventana.boton_limpiar.text().lower(),
        ventana.boton_eliminar.text().lower(),
        ventana.boton_volver.text().lower()
    ]

    for esperado in ["registrar", "modificar", "limpiar", "eliminar", "volver"]:
        assert esperado in nombres_botones, f"❌ Falta el botón: '{esperado}'"
