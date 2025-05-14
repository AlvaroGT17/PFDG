"""
Módulo de pruebas unitarias para `VentanaCargaGif`.

Este conjunto de pruebas valida el correcto funcionamiento de la ventana modal
de carga animada, utilizada en operaciones prolongadas del sistema como generación
de informes o cargas masivas.

Funciones cubiertas:
    - mostrar(): inicia el GIF y muestra la ventana centrada.
    - cerrar(): detiene el GIF y cierra la ventana.

Clases utilizadas:
    - VentanaCargaGif (desde `vistas.ventana_carga_gif`)
    - QLabel, QMovie (desde PySide6)

Autor: Cresnik
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QMovie
from pruebas.carga_gif_test import iniciar_ventana_carga_gif


def test_carga_gif_ventana_muestra(qtbot):
    """
    Verifica que al llamar a `mostrar()`, la ventana se hace visible.
    """
    ventana = iniciar_ventana_carga_gif()
    qtbot.addWidget(ventana)
    ventana.mostrar()

    assert ventana.isVisible()


def test_carga_gif_contiene_label(qtbot):
    """
    Verifica que la ventana contiene un QLabel configurado con una animación GIF.
    """
    ventana = iniciar_ventana_carga_gif()
    qtbot.addWidget(ventana)
    ventana.mostrar()

    label = ventana.findChild(QLabel)
    assert label is not None
    assert isinstance(label.movie(), QMovie)
    assert label.movie().fileName().endswith("gifcarga.gif")


def test_carga_gif_animacion_iniciada(qtbot):
    """
    Verifica que la animación del GIF se inicia correctamente al llamar a `mostrar()`.
    """
    ventana = iniciar_ventana_carga_gif()
    qtbot.addWidget(ventana)
    ventana.mostrar()

    assert ventana.movie.state() == QMovie.Running


def test_carga_gif_cerrar_detiene_animacion(qtbot):
    """
    Verifica que al llamar a `cerrar()`, la animación se detiene y la ventana se cierra.
    """
    ventana = iniciar_ventana_carga_gif()
    qtbot.addWidget(ventana)
    ventana.mostrar()

    assert ventana.movie.state() == QMovie.Running

    ventana.cerrar()

    assert ventana.movie.state() == QMovie.NotRunning
    assert not ventana.isVisible()
