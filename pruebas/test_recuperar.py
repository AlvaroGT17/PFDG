from PySide6.QtWidgets import QLineEdit, QPushButton
from pruebas.recuperar_test import iniciar_ventana_recuperar


def test_recuperar_campos_y_botones(qtbot):
    ventana = iniciar_ventana_recuperar()
    qtbot.addWidget(ventana)
    ventana.show()

    # Verificar que el campo de correo existe
    campo = ventana.findChild(QLineEdit)
    assert campo is not None
    assert campo.placeholderText() == "Introduce tu correo..."

    # Verificar botones
    botones = ventana.findChildren(QPushButton)
    textos = [btn.text().lower() for btn in botones]

    assert any("enviar" in texto for texto in textos)
    assert any("volver" in texto for texto in textos)
