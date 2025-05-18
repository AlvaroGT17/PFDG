"""
Tests para la ventana de login (`VentanaLogin`).

Este módulo valida la estructura y el comportamiento básico de la ventana
de inicio de sesión, asegurando que contiene los campos necesarios y 
gestiona correctamente tanto el cierre como los enlaces auxiliares.

Pruebas incluidas:
- Existencia de campos de usuario y contraseña.
- Presencia del botón "Entrar".
- Correcto funcionamiento del enlace de recuperación.
- Gestión del botón de salida.
- Control del evento de cierre con restricción o autorización.

"""

import pytest
from PySide6.QtWidgets import QLineEdit, QPushButton, QMessageBox
from vistas.ventana_login import VentanaLogin


def iniciar_ventana_login():
    """
    Crea una instancia de la ventana de login sin mostrarla en pantalla.

    :return: instancia de `VentanaLogin`
    """
    return VentanaLogin()


def test_login_campos_existentes(qtbot):
    """
    Verifica que la ventana de login contiene:
    - Un campo de texto para el usuario o nombre.
    - Un campo de texto para la contraseña.
    - Un botón de tipo "Entrar".
    """
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
    """
    Verifica que existe el enlace de recuperación de contraseña
    y que contiene el texto esperado (ej. "¿Olvidaste...?").
    """
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)

    assert ventana.enlace_recuperar is not None
    assert "olvidaste" in ventana.enlace_recuperar.text().lower()


def test_login_salir_cierra(qtbot):
    """
    Verifica que al pulsar el botón de salir se autoriza el cierre 
    y se oculta la ventana.
    """
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)

    ventana.salir_aplicacion()

    assert ventana.cierre_autorizado is True
    assert not ventana.isVisible()


def test_close_event_restringido(qtbot, mocker):
    """
    Simula un intento de cerrar la ventana sin autorización.
    Verifica que se lanza el aviso y se impide el cierre.
    """
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
    """
    Verifica que si `cierre_autorizado` es True, el evento `closeEvent`
    permite el cierre de la ventana sin restricciones.
    """
    ventana = iniciar_ventana_login()
    qtbot.addWidget(ventana)

    ventana.cierre_autorizado = True

    class EventoFalso:
        def ignore(self): ventana._cerrado = False
        def accept(self): ventana._cerrado = True

    evento = EventoFalso()
    ventana.closeEvent(evento)

    assert getattr(ventana, "_cerrado", False)
