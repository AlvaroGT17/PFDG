"""
Módulo de pruebas automáticas para la ventana de verificación de código (`VentanaVerificar`).

Este módulo realiza validaciones básicas sobre la interfaz gráfica correspondiente a la
pantalla de verificación de código enviado por correo electrónico.

Objetivos:
1. Verificar que la ventana se inicializa correctamente.
2. Asegurar que el botón "Verificar" está presente y correctamente etiquetado.

Dependencias necesarias:
- pytest
- pytest-qt
- PySide6

Forma parte del entorno de testeo del sistema ReyBoxes.
"""

import pytest
from pruebas.verificar_test import iniciar_ventana_verificar
from PySide6.QtWidgets import QPushButton


def test_ventana_verificar_se_inicializa(qtbot):
    """
    Verifica que la ventana de verificación se crea correctamente.

    Usa `qtbot` para agregar la instancia y comprobar que:
    - No es `None`.
    - Tiene un título asignado.

    Args:
        qtbot: Fixture de pytest-qt para manejar widgets en tests.

    Asserts:
        - La ventana debe existir.
        - Debe tener un título distinto de cadena vacía.
    """
    ventana = iniciar_ventana_verificar()
    qtbot.addWidget(ventana)

    assert ventana is not None, "❌ La ventana no se pudo crear"
    assert ventana.windowTitle() != "", "❌ La ventana no tiene título asignado"


def test_boton_verificar_existe(qtbot):
    """
    Verifica que la ventana contiene un botón etiquetado como "Verificar".

    Este botón es esencial para procesar el código OTP introducido por el usuario.
    La búsqueda se hace entre todos los QPushButton visibles.

    Args:
        qtbot: Fixture de pytest-qt.

    Asserts:
        - Debe existir al menos un botón cuyo texto contenga la palabra "verificar" (sin distinción de mayúsculas).
    """
    ventana = iniciar_ventana_verificar()
    qtbot.addWidget(ventana)

    botones = ventana.findChildren(QPushButton)
    assert any(
        "verificar" in b.text().lower() for b in botones
    ), "❌ No se encontró un botón con texto 'Verificar'"
