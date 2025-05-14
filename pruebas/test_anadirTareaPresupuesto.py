"""
Módulo de pruebas para el diálogo `DialogoTarea`.

Este módulo realiza pruebas unitarias utilizando `pytest-qt` para validar
el correcto funcionamiento del diálogo de introducción de tareas del sistema
de presupuestos. Las pruebas incluyen casos válidos, inválidos, validaciones visuales,
activación del botón aceptar y obtención de datos.

Clases probadas:
    - DialogoTarea (desde `vistas.ventana_anadirTareaPresupuesto`)

Requiere:
    - pytest
    - pytest-qt
    - PySide6

"""

from PySide6.QtWidgets import QLineEdit, QDialog
from vistas.ventana_anadirTareaPresupuesto import DialogoTarea


def test_dialogo_tarea_datos_correctos(qtbot):
    """
    Verifica que con datos válidos el método `obtener_datos` devuelva
    una tupla correcta con los valores esperados y el total calculado.
    """
    dialogo = DialogoTarea()
    qtbot.addWidget(dialogo)

    campos = dialogo.findChildren(QLineEdit)
    campo_tarea, campo_horas, campo_precio = campos[0], campos[1], campos[2]

    campo_tarea.setText("Cambiar frenos")
    campo_horas.setText("2")
    campo_precio.setText("30")

    datos = dialogo.obtener_datos()
    assert datos == ("Cambiar frenos", 2.0, 30.0, 60.0)


def test_dialogo_tarea_datos_invalidos(qtbot):
    """
    Verifica que con datos inválidos (texto no numérico, vacío o negativo),
    `obtener_datos` devuelve `None`.
    """
    dialogo = DialogoTarea()
    qtbot.addWidget(dialogo)

    campos = dialogo.findChildren(QLineEdit)
    campo_tarea, campo_horas, campo_precio = campos[0], campos[1], campos[2]

    campo_tarea.setText("")
    campo_horas.setText("abc")
    campo_precio.setText("-20")

    datos = dialogo.obtener_datos()
    assert datos is None


def test_boton_aceptar_se_activa(qtbot):
    """
    Verifica que el botón 'Aceptar' se activa cuando todos los datos
    ingresados son válidos.
    """
    dialogo = DialogoTarea()
    qtbot.addWidget(dialogo)

    dialogo.campo_tarea.setText("Aceite")
    dialogo.campo_horas.setText("1")
    dialogo.campo_precio.setText("10")

    assert dialogo.boton_aceptar.isEnabled()


def test_boton_aceptar_se_desactiva_si_campos_vacios(qtbot):
    """
    Verifica que el botón 'Aceptar' se desactiva cuando los campos están vacíos.
    """
    dialogo = DialogoTarea()
    qtbot.addWidget(dialogo)

    dialogo.campo_tarea.setText("")
    dialogo.campo_horas.setText("")
    dialogo.campo_precio.setText("")

    assert not dialogo.boton_aceptar.isEnabled()


def test_muestra_mensaje_error_precio(qtbot):
    """
    Verifica que al introducir un valor no numérico en el campo de precio,
    se muestra el mensaje de error correspondiente.
    """
    dialogo = DialogoTarea()
    qtbot.addWidget(dialogo)
    dialogo.show()
    qtbot.waitExposed(dialogo)

    dialogo.campo_precio.setText("abc")
    dialogo.validar_precio_en_tiempo_real()
    qtbot.wait(100)

    assert dialogo.mensaje_error_precio.isVisible()


def test_obtener_datos_campos_vacios(qtbot):
    """
    Verifica que `obtener_datos` retorna `None` si todos los campos están vacíos.
    """
    dialogo = DialogoTarea()
    qtbot.addWidget(dialogo)

    dialogo.campo_tarea.setText("")
    dialogo.campo_horas.setText("")
    dialogo.campo_precio.setText("")

    datos = dialogo.obtener_datos()
    assert datos is None


def test_validar_y_aceptar_con_datos_correctos(qtbot):
    """
    Verifica que si los datos son correctos y se llama a `validar_y_aceptar`,
    el diálogo se cierra con resultado `Accepted`.
    """
    dialogo = DialogoTarea()
    qtbot.addWidget(dialogo)

    dialogo.campo_tarea.setText("Cambio aceite")
    dialogo.campo_horas.setText("1.5")
    dialogo.campo_precio.setText("40")

    dialogo.validar_y_aceptar()
    assert dialogo.result() == QDialog.Accepted


def test_datos_limite_cero(qtbot):
    """
    Verifica que el sistema permite valores cero válidos en horas y precio.
    """
    dialogo = DialogoTarea()
    qtbot.addWidget(dialogo)

    dialogo.campo_tarea.setText("Tarea sin coste")
    dialogo.campo_horas.setText("0")
    dialogo.campo_precio.setText("0")

    datos = dialogo.obtener_datos()
    assert datos == ("Tarea sin coste", 0.0, 0.0, 0.0)
