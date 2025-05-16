"""
Pruebas unitarias para el diálogo de correo de presupuesto (`DialogoCorreoPresupuesto`).

Estas pruebas verifican:
- Que el diálogo se muestre correctamente.
- Que el campo de correo sea editable y refleje correctamente el valor introducido.

Se utilizan `qtbot` y PySide6 para simular la interacción con la interfaz gráfica.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

from PySide6.QtWidgets import QLineEdit
from pruebas.dialogoCorreoPresupuesto_test import iniciar_dialogo_correo_presupuesto


def test_dialogo_correo_se_muestra(qtbot):
    """
    Verifica que el diálogo de correo se muestra correctamente
    cuando se inicializa y se llama a `.show()`.
    """
    dialogo = iniciar_dialogo_correo_presupuesto()
    qtbot.addWidget(dialogo)
    dialogo.show()

    assert dialogo.isVisible()


def test_dialogo_correo_campo_editable(qtbot):
    """
    Verifica que el campo de correo sea editable y que el texto
    introducido se refleje correctamente mediante `obtener_correo()`.
    """
    dialogo = iniciar_dialogo_correo_presupuesto()
    qtbot.addWidget(dialogo)
    dialogo.show()

    campo = dialogo.findChild(QLineEdit)
    assert campo is not None

    texto_prueba = "cliente@ejemplo.com"
    campo.setText(texto_prueba)
    assert dialogo.obtener_correo() == texto_prueba
