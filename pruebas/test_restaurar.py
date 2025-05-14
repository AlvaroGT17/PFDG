from PySide6.QtWidgets import QLineEdit, QPushButton
from pruebas.restaurar_test import iniciar_ventana_restaurar


def test_restaurar_componentes_basicos(qtbot):
    ventana = iniciar_ventana_restaurar()
    qtbot.addWidget(ventana)
    ventana.show()

    # Verificar existencia de campos de contraseña
    campos = ventana.findChildren(QLineEdit)
    assert len(campos) >= 2
    assert campos[0].placeholderText().lower() == "nueva contraseña"
    assert campos[1].placeholderText().lower() == "repetir contraseña"

    # Verificar botones
    botones = ventana.findChildren(QPushButton)
    textos_botones = [btn.text().lower() for btn in botones]

    assert any("guardar" in texto for texto in textos_botones)
    assert any("volver" in texto for texto in textos_botones)
