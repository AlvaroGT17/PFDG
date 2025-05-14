"""
TESTS AUTOMÁTICOS: Ventana de gestión de vehículos

Este módulo contiene pruebas automatizadas para verificar que la interfaz
gráfica de la ventana de gestión de vehículos (VentanaVehiculos) se carga
correctamente y contiene los elementos esenciales de búsqueda.

Las pruebas están diseñadas para:
1. Asegurar que la ventana se inicializa sin errores.
2. Confirmar que existen campos de búsqueda funcionales con nombres intuitivos.

Dependencias:
- pytest
- pytest-qt
- PySide6
"""

import pytest
from pruebas.vehiculos_test import iniciar_ventana_vehiculos
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit

# ------------------------------------------------------------------------------
# TEST 1: Verificar que la ventana de vehículos se crea correctamente
# ------------------------------------------------------------------------------


def test_ventana_vehiculos_se_inicializa(qtbot):
    """
    TEST: Inicialización de VentanaVehiculos

    Crea una instancia de la ventana y la registra con qtbot
    (para manejo correcto en entorno de pruebas automáticas).

    Verifica que la ventana tiene un título asignado (indicador de
    que se inicializó correctamente y no está vacía o rota).

    Assertions:
    - El título de la ventana no debe ser una cadena vacía.
    """
    ventana = iniciar_ventana_vehiculos()  # Instancia sin mostrar
    qtbot.addWidget(ventana)               # Registra con qtbot (Pytest-Qt)

    assert ventana.windowTitle() != "", "La ventana no tiene título"


# ------------------------------------------------------------------------------
# TEST 2: Verificar que hay campos de búsqueda funcionales
# ------------------------------------------------------------------------------

def test_hay_campos_de_busqueda(qtbot):
    """
    TEST: Verificación de campos de búsqueda

    Comprueba que existen al menos dos campos de entrada (`QLineEdit`)
    en la ventana, y que al menos uno de ellos está relacionado con
    el nombre o identificación del cliente (por su `placeholderText`).

    Esto garantiza que el usuario pueda buscar por datos clave
    (nombre, cliente, etc.).

    Assertions:
    - Debe haber al menos 2 QLineEdit (campos de entrada).
    - Al menos uno de ellos debe tener como placeholder las palabras
      "nombre" o "cliente" (en minúsculas).

    Este test está diseñado para adaptarse a interfaces modernas,
    que usan placeholders en lugar de QLabel clásicos.
    """
    ventana = iniciar_ventana_vehiculos()
    qtbot.addWidget(ventana)

    # Obtener todos los campos QLineEdit de la ventana
    campos = ventana.findChildren(QLineEdit)
    assert len(campos) >= 2, "Faltan campos de entrada"

    # Extraer y limpiar los textos de placeholder
    placeholders = [c.placeholderText().lower()
                    for c in campos if c.placeholderText()]

    # Buscar palabras clave entre los placeholders
    assert any(
        "nombre" in p or "cliente" in p for p in placeholders
    ), "No hay placeholder de nombre o cliente"
