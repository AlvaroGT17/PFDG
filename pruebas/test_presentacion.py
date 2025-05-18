# pruebas/test_presentacion.py
"""
Pruebas para la ventana de presentación (`VentanaPresentacion`).

Este módulo comprueba el correcto comportamiento visual y lógico 
de la pantalla splash que se muestra al iniciar el sistema.

Objetivos:
- Verificar que la ventana se muestra correctamente.
- Comprobar sus configuraciones visuales (tamaño, transparencia, flags).
- Confirmar que se gestiona correctamente la transición a la ventana de login.
- Validar que el temporizador (`QTimer`) se activa para el cambio automático.

"""

from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from vistas.ventana_presentacion import VentanaPresentacion
from unittest.mock import patch


def test_presentacion_se_muestra(qtbot):
    """
    Verifica que la ventana de presentación se inicializa correctamente,
    es visible al mostrarse, y no abre la ventana de login durante el test.
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
    """
    Verifica que la ventana de presentación se configure sin bordes,
    con fondo translúcido y con la propiedad de mantenerse al frente.
    """
    with patch("vistas.ventana_presentacion.VentanaLogin"):
        ventana = VentanaPresentacion()
        qtbot.addWidget(ventana)

        assert ventana.windowFlags() & ventana.windowFlags().FramelessWindowHint
        assert ventana.windowFlags() & ventana.windowFlags().WindowStaysOnTopHint
        assert ventana.testAttribute(Qt.WA_TranslucentBackground)
        assert ventana.height() == 700


def test_presentacion_configuracion_dimensiones(qtbot):
    """
    Verifica que la ventana splash se muestra con dimensiones esperadas
    (ancho: 1000px, alto: 700px).
    """
    with patch("vistas.ventana_presentacion.VentanaLogin"):
        ventana = VentanaPresentacion()
        qtbot.addWidget(ventana)

        assert ventana.windowFlags() & ventana.windowFlags().FramelessWindowHint
        assert ventana.windowFlags() & ventana.windowFlags().WindowStaysOnTopHint
        assert ventana.testAttribute(Qt.WA_TranslucentBackground)

        assert ventana.width() == 1000
        assert ventana.height() == 700


def test_mostrar_login_lanza_login_y_cierra(qtbot):
    """
    Verifica que al ejecutar `mostrar_login`, se crea la ventana de login
    y se cierra la ventana de presentación.
    """
    with patch("vistas.ventana_presentacion.VentanaLogin") as mock_login:
        ventana = VentanaPresentacion()
        qtbot.addWidget(ventana)

        ventana.mostrar_login()

        mock_login.assert_called_once()
        assert not ventana.isVisible(), "❌ La ventana de presentación debería haberse cerrado"


def test_esperar_y_cambiar_lanza_timer(qtbot, mocker):
    """
    Comprueba que el método `esperar_y_cambiar()` activa correctamente
    un temporizador (`QTimer.singleShot`) configurado a 30ms.
    """
    ventana = VentanaPresentacion()
    single_shot_mock = mocker.patch.object(QTimer, "singleShot")

    ventana.esperar_y_cambiar()

    single_shot_mock.assert_called_once()
    assert single_shot_mock.call_args[0][0] == 30, "❌ Timer no configurado a 30ms"


def test_presentacion_instancia_basica(qtbot):
    """
    Verifica que la ventana puede instanciarse sin errores 
    y añadirse al entorno de pruebas Qt.
    """
    ventana = VentanaPresentacion()
    qtbot.addWidget(ventana)
