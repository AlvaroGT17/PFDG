# pruebas/test_presupuesto.py
"""
Pruebas para la interfaz `VentanaPresupuesto`.

Este módulo contiene tests que verifican el comportamiento y la estructura 
de la ventana de creación de presupuestos dentro del sistema ReyBoxes.

Se evalúan:
- Visibilidad y estado inicial de la ventana.
- Habilitación de botones.
- Añadir y eliminar tareas en la tabla.
- Actualización de costes totales y respuesta del cliente.
- Comportamiento del cierre forzado.
- Carga de datos de un presupuesto ya guardado.

Autor: Cresnik  
Proyecto: ReyBoxes - Taller Mecánico
"""

import pytest
from PySide6.QtWidgets import QDialogButtonBox, QTableWidgetItem
from vistas.ventana_presupuesto import VentanaPresupuesto


@pytest.fixture
def ventana(qtbot):
    """
    Crea una instancia de la ventana de presupuesto para pruebas.

    Añade el widget al entorno de QtBot y lo muestra antes del test.
    Se asegura de cerrar y liberar el widget tras cada prueba.
    """
    ventana = VentanaPresupuesto()
    qtbot.addWidget(ventana)
    ventana.show()
    yield ventana
    ventana.close()
    ventana.deleteLater()


def test_ventana_presupuesto_se_muestra(ventana):
    """
    Verifica que la ventana se muestre correctamente al instanciarla 
    y que el título sea el esperado.
    """
    assert ventana.isVisible()
    assert ventana.windowTitle() == "ReyBoxes - Presupuestos"


def test_botones_estan_desactivados_por_defecto(ventana):
    """
    Comprueba que los botones de guardar y añadir tarea están desactivados
    al iniciar la ventana, lo cual es el comportamiento esperado.
    """
    assert not ventana.boton_guardar.isEnabled()
    assert not ventana.boton_anadir_tarea.isEnabled()


def test_se_agrega_y_elimina_tarea(ventana):
    """
    Simula el flujo completo de añadir una tarea a la tabla 
    y posteriormente eliminarla, asegurando que la tabla refleja ambos cambios.
    """
    # Simula recepción válida para activar los botones
    ventana.combo_recepciones.addItem("Recepcion test")
    ventana.combo_recepciones.setCurrentIndex(1)
    ventana.controlador = type("Controlador", (), {"recepciones": [{
        "cliente": "Cliente Test",
        "matricula": "1234-ABC",
        "fecha": None,
        "precio_max_autorizado": 200.0,
        "observaciones": "Rev. general"
    }]})()
    ventana.recepcion_seleccionada(1)

    # Simula tarea añadida manualmente (sin usar el diálogo)
    fila = ventana.tabla_tareas.rowCount()
    ventana.tabla_tareas.insertRow(fila)
    ventana.tabla_tareas.setItem(fila, 0, QTableWidgetItem("Frenos"))
    ventana.tabla_tareas.setItem(fila, 1, QTableWidgetItem("2.0"))
    ventana.tabla_tareas.setItem(fila, 2, QTableWidgetItem("30.00 €"))
    ventana.tabla_tareas.setItem(fila, 3, QTableWidgetItem("60.00 €"))

    assert ventana.tabla_tareas.rowCount() == 1

    # Elimina la fila insertada
    ventana.tabla_tareas.selectRow(0)
    ventana.eliminar_tarea_seleccionada()
    assert ventana.tabla_tareas.rowCount() == 0


def test_coste_total_y_respuesta_cliente(ventana):
    """
    Verifica que al introducir tareas y un límite de precio,
    se actualiza el coste total y se selecciona automáticamente
    la respuesta del cliente (aceptado o rechazado).
    """
    ventana.campo_limite.setText("100.00 €")

    fila = ventana.tabla_tareas.rowCount()
    ventana.tabla_tareas.insertRow(fila)
    ventana.tabla_tareas.setItem(fila, 3, QTableWidgetItem("90.00 €"))
    ventana.actualizar_coste_total()

    assert ventana.campo_coste_total.text() == "90.00 €"
    assert ventana.combo_respuesta.currentText() == "Aceptado"


def test_control_cierre_con_flag(qtbot):
    """
    Simula el evento de cierre de la ventana verificando el uso del flag 
    `forzar_cierre` para aceptar o ignorar el evento de cierre.
    """
    ventana = VentanaPresupuesto()
    qtbot.addWidget(ventana)

    evento = type("FakeEvent", (), {
        "accept": lambda self: setattr(ventana, "_cerrado", True),
        "ignore": lambda self: setattr(ventana, "_cerrado", False)
    })()

    ventana.forzar_cierre = False
    ventana.closeEvent(evento)
    assert not getattr(ventana, "_cerrado", True)

    ventana.forzar_cierre = True
    ventana.closeEvent(evento)
    assert getattr(ventana, "_cerrado", False)


def test_cargar_presupuesto_datos(ventana):
    """
    Verifica que los datos de un presupuesto existente se cargan 
    correctamente en los campos correspondientes de la interfaz.
    """
    datos = {
        "cliente": "Juan Perez",
        "vehiculo": "Ford Focus",
        "fecha": None,
        "precio_max_autorizado": 250.00,
        "observaciones": "Chequeo completo",
        "tareas": [
            {"descripcion": "Cambio aceite", "horas": 1.0,
                "precio_hora": 35.0, "total": 35.0},
            {"descripcion": "Filtro aire", "horas": 0.5,
                "precio_hora": 20.0, "total": 10.0}
        ]
    }

    ventana.cargar_presupuesto(datos)

    assert ventana.campo_cliente.text() == "Juan Perez"
    assert ventana.tabla_tareas.rowCount() == 2
    assert "Chequeo completo" in ventana.texto_observaciones.toPlainText()
