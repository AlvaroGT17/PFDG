"""
TESTS AUTOMÁTICOS: Ventana de Reimpresión de Recepcionamientos

Este módulo valida la correcta creación y funcionalidad básica de la interfaz
gráfica `VentanaReimpresionRecepcionamiento`, usada para consultar y visualizar
documentos PDF de recepcionamiento.

Incluye pruebas para:
1. Verificar la correcta inicialización de la ventana.
2. Comprobar que existen botones esenciales como "Volver" o "Buscar".

Requisitos:
- pytest
- pytest-qt
- PySide6
"""

import pytest
from PySide6.QtWidgets import QToolButton
from vistas.ventana_reimpresionRecepcionamiento import VentanaReimpresionRecepcionamiento


def iniciar_ventana_reimpresion():
    """
    Crea una instancia simulada de la ventana de reimpresión de recepcionamientos.

    Returns:
        VentanaReimpresionRecepcionamiento: Instancia lista para pruebas.
    """
    nombre_ficticio = "CRESNIK"
    rol_ficticio = "Administrador"
    def callback_falso(): return None  # Función simulada

    return VentanaReimpresionRecepcionamiento(
        nombre_ficticio, rol_ficticio, callback_falso
    )


def test_ventana_se_inicializa_correctamente(qtbot):
    """
    TEST 1: Inicialización básica

    Verifica que la ventana puede ser creada sin errores y que contiene un título visible.
    """
    ventana = iniciar_ventana_reimpresion()
    qtbot.addWidget(ventana)

    assert ventana is not None, "La ventana no se pudo crear"
    assert ventana.windowTitle() != "", "La ventana no tiene título definido"


def test_existe_boton_importante(qtbot):
    """
    TEST 2: Presencia de botón funcional

    Verifica que la ventana contiene al menos un botón principal:
    - Volver (para regresar al menú)
    - Buscar (si existiera en el futuro)

    Se inspeccionan los `QToolButton` disponibles en la interfaz.
    """
    ventana = iniciar_ventana_reimpresion()
    qtbot.addWidget(ventana)

    botones = ventana.findChildren(QToolButton)
    textos = [b.text().lower() for b in botones]

    print("🧪 Botones encontrados en la interfaz:")
    for b in botones:
        print(f" - {b.objectName() or '[sin nombre]'}: '{b.text()}'")

    assert any("buscar" in t or "volver" in t for t in textos), \
        "No se encontró un botón con texto 'Buscar' o 'Volver'"
