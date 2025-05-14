# pruebas/test_recepcionamiento.py

"""
Test automatizado de interfaz para `VentanaRecepcionamiento`.

Objetivos:
- Verificar que la ventana se inicializa correctamente.
- Validar que el título no está vacío.
"""

import pytest
from PySide6.QtWidgets import QLineEdit
from pruebas.recepcionamiento_test import iniciar_ventana_recepcionamiento


def test_recepcionamiento_se_inicializa(qtbot):
    """
    Verifica que la ventana se carga y tiene un título válido.
    """
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)

    assert ventana.windowTitle() != "", "La ventana no tiene título definido."


def test_campos_principales_estan_poblados(qtbot):
    """
    Asegura que los campos importantes como nombre y matrícula están rellenados en los datos simulados.
    """
    ventana = iniciar_ventana_recepcionamiento()
    qtbot.addWidget(ventana)

    assert ventana.input_nombre.text() != "", "El campo de nombre está vacío"
    assert ventana.input_matricula.currentText() != "", "El campo matrícula está vacío"
