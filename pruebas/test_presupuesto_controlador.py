# pruebas/test_presupuesto_controlador.py
"""
Tests para el controlador de presupuestos (`PresupuestoControlador`).

Este módulo valida el comportamiento del controlador encargado de gestionar
la lógica relacionada con la creación de presupuestos, incluyendo:

- La correcta inicialización y enlace con la vista.
- La carga de recepciones disponibles para selección.
- La generación del archivo PDF simulado a partir de datos de ejemplo.

Autor: Cresnik  
Proyecto: ReyBoxes - Gestión de Taller Mecánico
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from controladores.presupuesto_controlador import PresupuestoControlador
from vistas.ventana_presupuesto import VentanaPresupuesto


@pytest.fixture(autouse=True)
def evitar_mostrar_qt(monkeypatch):
    """
    Evita que las ventanas se muestren gráficamente durante los tests,
    sobrescribiendo el método `show()` de QWidget.
    """
    monkeypatch.setattr("PySide6.QtWidgets.QWidget.show", lambda self: None)


@pytest.fixture
def mock_ventana(qtbot):
    """
    Crea una instancia simulada de `VentanaPresupuesto` para pruebas.

    Se asegura de agregar la ventana al entorno de pruebas Qt y cerrarla correctamente al finalizar.
    """
    ventana = VentanaPresupuesto()
    qtbot.addWidget(ventana)
    yield ventana
    ventana.close()
    ventana.deleteLater()


def test_init_conecta_controlador_y_boton(mock_ventana):
    """
    Verifica que al inicializar el `PresupuestoControlador`, este se conecta
    correctamente con la vista, asigna su referencia, y prepara las recepciones.
    """
    with patch("controladores.presupuesto_controlador.obtener_recepciones_para_presupuesto", return_value=[]):
        controlador = PresupuestoControlador(mock_ventana)
        assert controlador.ventana == mock_ventana
        assert hasattr(mock_ventana, "controlador")
        assert isinstance(controlador.recepciones, list)


def test_cargar_recepciones_vacia(mock_ventana):
    """
    Comprueba el comportamiento del controlador cuando no hay recepciones disponibles:
    se debe deshabilitar el combo y mostrar un mensaje indicativo.
    """
    with patch("controladores.presupuesto_controlador.obtener_recepciones_para_presupuesto", return_value=[]):
        controlador = PresupuestoControlador(mock_ventana)
        assert mock_ventana.combo_recepciones.count() == 1
        assert mock_ventana.combo_recepciones.currentText() == "No hay recepciones disponibles"
        assert not mock_ventana.combo_recepciones.isEnabled()


def test_generar_pdf_presupuesto_crea_archivo(tmp_path):
    """
    Verifica que el método `generar_pdf_presupuesto` genera correctamente un archivo PDF
    simulado a partir de los datos del presupuesto, utilizando mocks para evitar
    el renderizado y la escritura real del archivo.

    Se comprueba que el método `write_pdf` se ha llamado una vez y que la ruta termina en `.pdf`.
    """
    datos = {
        "cliente": "Juan Pérez",
        "matricula": "1234ABC",
        "fecha_recepcion": "01/01/2025 10:00",
        "precio_max": "500.00",
        "respuesta_cliente": "Aceptado",
        "observaciones": "Revisión general",
        "total_estimado": "450.00",
        "tareas": [
            {"descripcion": "Cambio de aceite", "horas": 1.5,
                "precio_hora": 40, "total": 60},
            {"descripcion": "Filtro aire", "horas": 1,
                "precio_hora": 30, "total": 30}
        ]
    }

    with patch("controladores.presupuesto_controlador.Template.render", return_value="<html></html>"), \
            patch("controladores.presupuesto_controlador.HTML.write_pdf") as mock_write, \
            patch("controladores.presupuesto_controlador.os.makedirs"):

        controlador = PresupuestoControlador(MagicMock())
        ruta = controlador.generar_pdf_presupuesto(datos)

    mock_write.assert_called_once()
    assert ruta.endswith(".pdf")
