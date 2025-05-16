"""
Pruebas unitarias para la clase VentanaFichar.

Se valida el comportamiento de la interfaz de fichaje de personal, incluyendo:
- Carga correcta de la ventana.
- Visualización de hora actual.
- Selección de tipo de fichaje (Entrada / Salida).
- Funciones de confirmación y advertencia.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

from PySide6.QtTest import QTest
import pytest
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from pruebas.fichar_test import iniciar_ventana_fichar


def test_fichar_se_instancia_correctamente(qtbot):
    """
    Verifica que el controlador de fichaje se instancia correctamente
    y contiene una ventana funcional.
    """
    controlador = iniciar_ventana_fichar()
    qtbot.addWidget(controlador.ventana)

    assert controlador is not None
    assert hasattr(controlador, "ventana")


def test_reloj_se_actualiza(qtbot):
    """
    Verifica que el reloj se inicializa con un valor válido en formato HH:mm:ss.
    """
    controlador = iniciar_ventana_fichar()
    qtbot.addWidget(controlador.ventana)

    texto_reloj = controlador.ventana.reloj_label.text()
    assert len(texto_reloj) == 8  # "HH:mm:ss"
    assert texto_reloj.count(":") == 2


def test_opciones_radio_funcionan(qtbot):
    """
    Verifica que al seleccionar Entrada o Salida, el método `obtener_tipo_fichaje`
    devuelve correctamente el valor correspondiente.
    """
    controlador = iniciar_ventana_fichar()
    qtbot.addWidget(controlador.ventana)

    ventana = controlador.ventana
    ventana.radio_entrada.setChecked(True)
    assert ventana.obtener_tipo_fichaje() == "ENTRADA"

    ventana.radio_salida.setChecked(True)
    assert ventana.obtener_tipo_fichaje() == "SALIDA"


def test_opcion_radio_no_seleccionada(qtbot):
    """
    Verifica que si no hay ningún radio seleccionado, `obtener_tipo_fichaje`
    devuelve `None`.
    """
    controlador = iniciar_ventana_fichar()
    qtbot.addWidget(controlador.ventana)

    ventana = controlador.ventana
    ventana.radio_entrada.setChecked(False)
    ventana.radio_salida.setChecked(False)

    assert ventana.obtener_tipo_fichaje() is None


def test_mostrar_confirmacion_y_error(qtbot, mocker):
    """
    Verifica que se llaman correctamente los cuadros de diálogo para error e información.
    """
    controlador = iniciar_ventana_fichar()
    qtbot.addWidget(controlador.ventana)

    ventana = controlador.ventana
    mock_warning = mocker.patch.object(QMessageBox, "warning")
    mock_info = mocker.patch.object(QMessageBox, "information")

    ventana.mostrar_error("Prueba de error")
    ventana.mostrar_confirmacion("Prueba de confirmación")

    mock_warning.assert_called_once_with(
        ventana, "Fichaje inválido", "Prueba de error")
    mock_info.assert_called_once_with(
        ventana, "Fichaje registrado", "Prueba de confirmación")


def test_confirmar_sin_seleccion_muestra_advertencia(qtbot, mocker):
    """
    Verifica que al pulsar el botón Confirmar sin seleccionar entrada o salida,
    se muestra una advertencia.
    """
    controlador = iniciar_ventana_fichar()
    ventana = controlador.ventana
    qtbot.addWidget(ventana)

    # Mockear el QMessageBox.warning
    mock_warning = mocker.patch.object(QMessageBox, "warning")

    # Asegurarse de que nada está seleccionado
    ventana.radio_entrada.setChecked(False)
    ventana.radio_salida.setChecked(False)

    # Simular clic en Confirmar
    qtbot.mouseClick(ventana.btn_confirmar, Qt.LeftButton)

    mock_warning.assert_called_once_with(
        ventana, "Fichaje inválido", "Debes seleccionar 'Entrada' o 'Salida'"
    )


def test_confirmar_con_entrada_muestra_confirmacion(qtbot, mocker):
    """
    Verifica que al pulsar Confirmar con 'Entrada' seleccionada,
    se muestra un mensaje de confirmación.
    """
    controlador = iniciar_ventana_fichar()
    ventana = controlador.ventana
    qtbot.addWidget(ventana)

    mock_info = mocker.patch.object(QMessageBox, "information")

    ventana.radio_entrada.setChecked(True)

    qtbot.mouseClick(ventana.btn_confirmar, Qt.LeftButton)

    mock_info.assert_called_once_with(
        ventana, "Fichaje registrado", "Fichaje de ENTRADA registrado correctamente."
    )


def test_confirmar_con_salida_muestra_confirmacion(qtbot, mocker):
    """
    Verifica que al pulsar Confirmar con 'Salida' seleccionada,
    se muestra un mensaje de confirmación.
    """
    controlador = iniciar_ventana_fichar()
    ventana = controlador.ventana
    qtbot.addWidget(ventana)

    mock_info = mocker.patch.object(QMessageBox, "information")

    ventana.radio_salida.setChecked(True)

    qtbot.mouseClick(ventana.btn_confirmar, Qt.LeftButton)

    mock_info.assert_called_once_with(
        ventana, "Fichaje registrado", "Fichaje de SALIDA registrado correctamente."
    )
