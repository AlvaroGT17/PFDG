import pytest
from PySide6.QtWidgets import QLineEdit, QPushButton, QMessageBox
from vistas.ventana_login import VentanaLogin


def iniciar_ventana_login():
    return VentanaLogin()


def test_login_campos_existentes(qtbot):
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)

    campos = ventana.findChildren(QLineEdit)
    placeholders = [c.placeholderText().lower() for c in campos]

    assert any(
        "usuario" in ph or "nombre" in ph for ph in placeholders), "❌ Falta el campo de usuario"
    assert any(
        "contraseña" in ph for ph in placeholders), "❌ Falta el campo de contraseña"

    botones = ventana.findChildren(QPushButton)
    textos = [b.text().lower() for b in botones]
    assert any("entrar" in txt for txt in textos), "❌ Falta el botón de entrar"


def test_login_enlace_recuperacion(qtbot):
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)
    assert ventana.enlace_recuperar is not None
    assert "olvidaste" in ventana.enlace_recuperar.text().lower()


def test_login_salir_cierra(qtbot):
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)

    # Simula hacer clic en el botón salir
    ventana.salir_aplicacion()

    assert ventana.cierre_autorizado is True
    assert not ventana.isVisible()  # Se debería cerrar


def test_close_event_restringido(qtbot, mocker):
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)

    mock_msg = mocker.patch.object(QMessageBox, "information")

    ventana.cierre_autorizado = False

    class EventoFalso:
        def ignore(self): ventana._cerrado = False
        def accept(self): ventana._cerrado = True

    evento = EventoFalso()
    ventana.closeEvent(evento)

    mock_msg.assert_called_once()
    assert not getattr(ventana, "_cerrado", True)


def test_close_event_autorizado(qtbot):
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)

    ventana.cierre_autorizado = True

    class EventoFalso:
        def ignore(self): ventana._cerrado = False
        def accept(self): ventana._cerrado = True

    evento = EventoFalso()
    ventana.closeEvent(evento)

    assert getattr(ventana, "_cerrado", False)
