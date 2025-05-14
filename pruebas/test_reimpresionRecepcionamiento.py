"""
TEST AUTOMATIZADO: Ventana de reimpresión de recepcionamientos

Este test verifica que la ventana `VentanaReimpresionRecepcionamiento`:

- Se puede instanciar correctamente sin errores.
- Tiene un título definido.
- Contiene elementos básicos como botones funcionales.

Se utiliza `pytest-qt` para trabajar con elementos de PySide6 sin mostrar la ventana.
"""

import pytest
from PySide6.QtWidgets import QToolButton
from vistas.ventana_reimpresionRecepcionamiento import VentanaReimpresionRecepcionamiento


def iniciar_ventana_reimpresion():
    """
    Crea una instancia de la ventana de reimpresión para pruebas automatizadas.
    No la muestra visualmente. Simula parámetros mínimos.
    """
    nombre_ficticio = "CRESNIK"
    rol_ficticio = "Administrador"
    def callback_falso(): return None  # Función vacía simulando volver_callback

    return VentanaReimpresionRecepcionamiento(
        nombre_ficticio, rol_ficticio, callback_falso
    )


def test_ventana_se_inicializa_correctamente(qtbot):
    """
    Verifica que la ventana se instancia sin errores y tiene título.
    """
    ventana = iniciar_ventana_reimpresion()
    qtbot.addWidget(ventana)

    assert ventana is not None
    assert ventana.windowTitle() != ""


def test_existe_boton_buscar_o_volver(qtbot):
    """
    Comprueba que existe al menos un botón importante como 'Buscar' o 'Volver'.
    """
    ventana = iniciar_ventana_reimpresion()
    qtbot.addWidget(ventana)

    botones = ventana.findChildren(QToolButton)
    textos = [b.text().lower() for b in botones]

    print("🧪 Botones encontrados:")

    for b in botones:
        print(f"- {b.objectName() or '[sin nombre]'}: '{b.text()}'")

    assert any("buscar" in t or "volver" in t for t in textos), \
        "No se encontró un botón 'Buscar' o 'Volver' en la ventana."
