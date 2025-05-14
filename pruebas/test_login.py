# pruebas/test_login.py
from PySide6.QtWidgets import QLineEdit, QPushButton
from vistas.ventana_login import VentanaLogin


def iniciar_ventana_login():
    return VentanaLogin()


def test_login_campos_existentes(qtbot):
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)

    # Buscar campos por placeholder
    campos = ventana.findChildren(QLineEdit)
    placeholders = [c.placeholderText().lower() for c in campos]

    assert any(
        "usuario" in ph or "nombre" in ph for ph in placeholders), "❌ Falta el campo de usuario"
    assert any(
        "contraseña" in ph for ph in placeholders), "❌ Falta el campo de contraseña"

    # Buscar botón con texto "Entrar"
    botones = ventana.findChildren(QPushButton)
    textos = [b.text().lower() for b in botones]
    assert any("entrar" in txt for txt in textos), "❌ Falta el botón de entrar"
