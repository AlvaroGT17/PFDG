# pruebas/test_presentacion.py
"""
Pruebas para la ventana de presentación (`VentanaPresentacion`).

Objetivo:
- Verificar que la ventana splash se muestra correctamente y es visible.
- Impedir que durante el test se abra automáticamente la ventana de login.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from vistas.ventana_presentacion import VentanaPresentacion
from unittest.mock import patch


def test_presentacion_se_muestra(qtbot):
    """
    Verifica que la ventana de presentación se inicia correctamente,
    se muestra con tamaño válido y no lanza la ventana de login durante el test.
    """
    # 🧪 Parcheamos VentanaLogin para que no se abra realmente
    with patch("vistas.ventana_presentacion.VentanaLogin") as mock_login:
        ventana = VentanaPresentacion()
        qtbot.addWidget(ventana)

        ventana.show()
        qtbot.waitExposed(ventana)

        assert ventana.isVisible(), "❌ La ventana no está visible"
        assert ventana.width() > 0 and ventana.height() > 0, "❌ Dimensiones incorrectas"
        assert not mock_login.called, "❌ No debería abrirse VentanaLogin en este test"


def test_presentacion_configuracion_inicial(qtbot):
    with patch("vistas.ventana_presentacion.VentanaLogin"):
        ventana = VentanaPresentacion()
        qtbot.addWidget(ventana)

        assert ventana.windowFlags() & ventana.windowFlags().FramelessWindowHint
        assert ventana.windowFlags() & ventana.windowFlags().WindowStaysOnTopHint
        assert ventana.testAttribute(Qt.WA_TranslucentBackground)
        assert ventana.height() == 700


def test_presentacion_configuracion_inicial(qtbot):
    with patch("vistas.ventana_presentacion.VentanaLogin"):
        ventana = VentanaPresentacion()
        qtbot.addWidget(ventana)

        assert ventana.windowFlags() & ventana.windowFlags().FramelessWindowHint
        assert ventana.windowFlags() & ventana.windowFlags().WindowStaysOnTopHint
        assert ventana.testAttribute(Qt.WA_TranslucentBackground)

        assert ventana.width() == 1000
        assert ventana.height() == 700


def test_mostrar_login_lanza_login_y_cierra(qtbot):
    with patch("vistas.ventana_presentacion.VentanaLogin") as mock_login:
        ventana = VentanaPresentacion()
        qtbot.addWidget(ventana)

        ventana.mostrar_login()

        mock_login.assert_called_once()
        assert not ventana.isVisible(), "❌ La ventana de presentación debería haberse cerrado"


def test_esperar_y_cambiar_lanza_timer(qtbot, mocker):
    ventana = VentanaPresentacion()
    single_shot_mock = mocker.patch.object(QTimer, "singleShot")

    ventana.esperar_y_cambiar()

    single_shot_mock.assert_called_once()
    assert single_shot_mock.call_args[0][0] == 30, "❌ Timer no configurado a 30ms"


def test_presentacion_instancia_basica(qtbot):
    ventana = VentanaPresentacion()
    qtbot.addWidget(ventana)
